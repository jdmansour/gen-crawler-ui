""" Views for the crawls app. """
# pylint: disable=too-many-ancestors

import json
import logging
import os
import time
import threading
from typing import Any, Generator, Iterator, Optional

import redis
import redis.client
import requests
from crawls.forms import StartCrawlForm
from crawls.models import Crawler, CrawlJob, FilterRule, FilterSet, SourceItem
from crawls.serializers import (CrawlerSerializer, FilterRuleSerializer,
                                FilterSetSerializer, SourceItemSerializer)
from crawls.fields_processor import FieldsProcessor
from django.conf import settings
from django.contrib import messages
from django.http import StreamingHttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, FormView, ListView
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from test_aggregator import HelperAggregator

log = logging.getLogger(__name__)


class EventAggregator:
    """
    Aggregiert Events um zu vermeiden, dass zu viele Events an das Frontend gesendet werden.
    
    Strategie:
    - Sammelt Events für eine bestimmte Zeit (debounce_ms)
    - Sendet nur das neueste Event nach der Wartezeit
    - Sendet spätestens nach max_wait_ms ein Event, auch wenn noch neue ankommen
    - Sendet sofort finale Events (wie "finished", "error")
    """
    
    def __init__(self, send_callback, debounce_ms=200, max_wait_ms=2000):
        self.send_callback = send_callback
        self.debounce_ms = debounce_ms / 1000.0  # Convert to seconds
        self.max_wait_ms = max_wait_ms / 1000.0
        self.pending_event = None
        self.timer = None
        self.first_event_time = None
        self.lock = threading.Lock()
        self._shutdown = False
        
    def add_event(self, event_data):
        """Fügt ein neues Event hinzu und verwaltet das Timing."""
        if self._shutdown:
            return
            
        with self.lock:
            if self._shutdown:
                return
                
            current_time = time.time()
            
            # Finale Events sofort senden
            if self._is_final_event(event_data):
                self._cancel_timer()
                self._send_event(event_data)
                return
            
            # Erstes Event in dieser Batch?
            if self.pending_event is None:
                self.first_event_time = current_time
            
            # Event speichern (überschreibt vorheriges)
            self.pending_event = event_data
            
            # Prüfen ob max_wait_ms erreicht wurde
            if (self.first_event_time and 
                current_time - self.first_event_time >= self.max_wait_ms):
                self._cancel_timer()
                self._send_pending_event()
                return
            
            # Timer zurücksetzen
            self._cancel_timer()
            if not self._shutdown:
                self.timer = threading.Timer(self.debounce_ms, self._send_pending_event)
                self.timer.start()
    
    def _is_final_event(self, event_data):
        """Prüft ob es sich um ein finales Event handelt, das sofort gesendet werden soll."""
        if event_data.get('type') == 'crawl_job_update':
            crawl_job = event_data.get('crawl_job', {})
            state = crawl_job.get('state', '')
            return state in ['finished', 'error', 'cancelled', 'failed']
        return event_data.get('type') in ['error', 'complete', 'finished']
    
    def _send_pending_event(self):
        """Sendet das ausstehende Event."""
        if self._shutdown:
            return
            
        with self.lock:
            if self._shutdown:
                return
                
            if self.pending_event:
                self._send_event(self.pending_event)
                self._reset_state()
    
    def _send_event(self, event_data):
        """Sendet ein Event über den Callback."""
        if self._shutdown:
            return
            
        try:
            # Aktualisiere Timestamp vor dem Senden
            event_data['timestamp'] = time.time()
            self.send_callback(event_data)
            log.debug("Aggregated event sent: %s", event_data.get('type', 'unknown'))
        except Exception as e:
            log.error("Error sending aggregated event: %s", e)
    
    def _cancel_timer(self):
        """Bricht den aktuellen Timer ab."""
        if self.timer:
            self.timer.cancel()
            self.timer = None
    
    def _reset_state(self):
        """Setzt den internen Zustand zurück."""
        self.pending_event = None
        self.first_event_time = None
    
    def flush_pending(self):
        """Sendet ein ausstehende Event sofort."""
        with self.lock:
            if self.pending_event and not self._shutdown:
                self._cancel_timer()
                self._send_event(self.pending_event)
                self._reset_state()
    
    def cleanup(self):
        """Räumt Ressourcen auf."""
        self._shutdown = True
        with self.lock:
            self._cancel_timer()
            # Letztes Event noch senden, falls vorhanden
            if self.pending_event:
                try:
                    self._send_event(self.pending_event)
                except Exception as e:
                    log.error("Error sending final event during cleanup: %s", e)
            self._reset_state()


class SourceItemViewSet(viewsets.ModelViewSet):
    """ Provides the API under /api/source_items/ """
    queryset = SourceItem.objects.all()
    serializer_class = SourceItemSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'guid'

    @action(detail=True, methods=['get'])
    def inheritable_fields(self, request, guid: str):
        """ Returns a list of inheritable fields for this source item. Lives at
            http://127.0.0.1:8000/api/source_items/<guid>/inheritable_fields/ """
        
        fp = FieldsProcessor()
        result = fp.process(guid)
        return Response(result)
    

class CrawlerViewSet(viewsets.ModelViewSet):
    """ Provides the API under /api/crawlers/ """
    queryset = Crawler.objects.all()
    serializer_class = CrawlerSerializer
    # TODO: restrict to authenticated users!
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['post'])
    def start_crawl(self, request, pk=None):
        print("start_crawl called")
        print("pk:", pk)
        obj = self.get_object()
        print("Crawler:", obj)
        parameters = {
            'project': 'scraper',
            'spider': 'example',
            'start_url': obj.start_url,
            'follow_links': True,
            'crawler_id': str(obj.id),
        }
        # get SCRAPYD_URL from settings
        url = settings.SCRAPYD_URL + "/schedule.json"
        response = requests.post(url, data=parameters, timeout=5)
        log.info("Response: %s", response.text)
        log.info("Status code: %s", response.status_code)
        if response.status_code != 200:
            return Response({'status': 'error', 'message': response.text}, status=500)
        else:
            obj = response.json()
            return Response(obj)


@csrf_exempt
def crawler_status_stream(request, crawler_id):
    """
    Server-Sent Events endpoint for real-time crawler status updates.
    Listens to Redis pub/sub for crawler status changes.
    Uses EventAggregator to reduce event frequency.
    """
    log.info("crawler_status_stream called")
    log.info("Request: %s", request)
    log.info("crawler_id: %s", crawler_id)
    log.info("Thread ID in request handler: %s", threading.get_ident())
    crawler = get_object_or_404(Crawler, pk=crawler_id)
    
    # Get Redis connection from environment
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    redis_client = redis.from_url(redis_url)
    pubsub = redis_client.pubsub()
    channel_name = f'crawler_status_{crawler_id}'
    pubsub.subscribe(channel_name)
    
    def event_stream():
        event_queue = []
        aggregator = None
        log.info("Event stream started for crawler %s", crawler_id)
        log.info("Thread ID in StreamingHttpResponse generator: %s", threading.get_ident())

        def send_event(event_data):
            event_queue.append(f"data: {json.dumps(event_data)}\n\n".encode('utf-8'))
   
        try:
            aggregator = HelperAggregator(
                callback=send_event,
                debounce_ms=200,
                max_wait_ms=1000
            )

            while pubsub.subscribed:
                # If there are pending events, use a short timeout so we can get to "yield event"
                # and are not stuck waiting for new messages from Redis.
                # If there are no events in the aggregator, then we can wait longer for new messages.
                timeout = 0.1 if len(aggregator.events) > 0 else None
                message = pubsub.handle_message(pubsub.parse_response(timeout=timeout, block=False))  # type: ignore
                
                # Sende alle gepufferten Events
                while event_queue:
                    event = event_queue.pop(0)
                    log.info("Sending event from queue: %s", event)
                    yield event
        
                if message is None:
                    log.info("Timeout")
                    continue
                    
                if message['type'] != 'message':
                    log.info("Ignoring non-message type: %s", message['type'])
                    continue

                try:
                    data = json.loads(message['data'].decode('utf-8'))
                    log.info("Received Redis message: %s", data.get('type', 'unknown'))
                    # Event über Aggregator verarbeiten
                    aggregator.add_event(data)
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    log.error("Error processing Redis message: %s", e)
                    continue
                        
        except Exception as e:
            log.exception("Error in crawler status stream: '%r', %s", e, str(e))
            error_data = {
                'type': 'error',
                'message': str(e),
                'timestamp': time.time()
            }
            yield f"data: {json.dumps(error_data)}\n\n".encode('utf-8')
        finally:
            pubsub.close()
            log.info("Event stream for crawler %s closed", crawler_id)
    
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Cache-Control'
    return response


class FilterSetViewSet(viewsets.ModelViewSet):
    """ Provides the API under /api/filter_sets/ """
    queryset = FilterSet.objects.all()
    serializer_class = FilterSetSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def unmatched(self, request, pk=None):
        """ Returns a list of unmatched URLs. Lives at
            http://127.0.0.1:8000/api/filter_sets/1/unmatched/ """

        # pylint: disable=unused-argument
        qs = self.get_object().crawl_job.crawled_urls
        for rule in self.get_object().rules.all():
            qs = qs.exclude(url__startswith=rule.rule)
        qs = qs.all()
        urls = qs[:30].values_list('url', flat=True)
        is_complete = urls.count() == qs.count()

        result = {
            "is_complete": is_complete,
            "total_count": qs.count(),
            "unmatched_urls": urls,
        }
        return Response(result)


class FilterRuleViewSet(viewsets.ModelViewSet):
    """ Provides the API under /api/filter_rules/ """
    queryset = FilterRule.objects.all()
    serializer_class = FilterRuleSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).order_by('position')

    # run code when a new rule is created
    def perform_create(self, serializer: FilterRuleSerializer):  # type: ignore[override]
        """ Run when a new rule is created. """
        rule = serializer.save()
        rule.filter_set.evaluate()
        # TODO: in what is returned in the request, the new count is not reflected yet (?)
        rule.save()  # ?

    def perform_update(self, serializer: FilterRuleSerializer):  # type: ignore[override]
        """ Run when a rule is updated. """
        log.info("perform_update")
        rule = serializer.save()
        rule.filter_set.evaluate(rule)
        log.info("Rule %r updated", rule)
        # rule.save()

    # add endpoint under filter_rules/<id>/matches to get all matching URLs
    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        """ Returns a list of URLs that match this rule. Lives at
            http://127.0.0.1:8000/api/filter_rules/1/matches/ """

        # pylint: disable=unused-argument
        rule = self.get_object()

        # get previous rules, when sorted by position
        previous_rules = rule.filter_set.rules.filter(
            position__lt=rule.position)

        # get all URLs that match this rule and any of the previous rules
        qs = rule.filter_set.crawl_job.crawled_urls
        for r in previous_rules:
            qs = qs.exclude(url__startswith=r.rule)
        new_matches = qs.filter(url__startswith=rule.rule)
        other_matches = rule.filter_set.crawl_job.crawled_urls.filter(
            url__startswith=rule.rule).exclude(pk__in=new_matches)
        result = {
            'new_matches': [url.url for url in new_matches],
            'other_matches': [url.url for url in other_matches],
        }

        # matches = rule.filter_set.crawl_job.crawled_urls.filter(url__startswith=rule.rule)
        # result = {
        #     'matches': [url.url for url in matches],
        # }
        return Response(result)


class CrawlsListView(ListView):
    model = CrawlJob
    template_name = 'crawls_list.html'
    context_object_name = 'crawls'

    def get_queryset(self):
        return CrawlJob.objects.all().order_by('-created_at')


class CrawlDetailView(DetailView):
    model = CrawlJob
    template_name = 'crawl_detail.html'
    context_object_name = 'crawl'


class FilterSetDetailView(DetailView):
    model = FilterSet
    template_name = 'filterset_detail.html'
    context_object_name = 'filterset'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FilterSetCreateView(CreateView):
    model = FilterSet
    fields = ['name', 'crawl_job']
    template_name = 'filterset_create.html'
    # success_url = '/crawls/'
    object: Optional[FilterSet]

    def get_success_url(self) -> str:
        # return the new filter set's detail page
        assert self.object is not None
        return reverse_lazy('filter_details', kwargs={'pk': self.object.pk})

    # get crawl job id from URL
    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial().copy()
        # get crawl_job_id from GET parameters
        crawl_job_id = self.request.GET.get('crawl_job_id')
        # Raise error if crawl_job_id is not provided
        if crawl_job_id is None:
            raise ValueError("crawl_job_id is required")
        initial['crawl_job'] = crawl_job_id
        return initial

    # run code on successful form submission
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, 'Filter set created')
        return response


class HealthViewSet(viewsets.ViewSet):
    """ Provides the API under /api/health/ """

    permission_classes = [permissions.AllowAny]

    def list(self, request):
        """ Return health status. """
        return Response({'status': 'ok'})


class StartCrawlFormView(FormView):
    """ Start a new crawl job. """

    template_name = 'start_crawl.html'
    form_class = StartCrawlForm
    success_url = '/crawls/'

    def form_valid(self, form: StartCrawlForm):
        start_url = form.cleaned_data['start_url']
        follow_links = form.cleaned_data['follow_links']
        parameters = {
            'project': 'scraper',
            'spider': 'example',
            'start_url': start_url,
            'follow_links': follow_links,
        }
        # get SCRAPYD_URL from settings
        url = settings.SCRAPYD_URL + "/schedule.json"
        response = requests.post(url, data=parameters, timeout=5)
        log.info("Response: %s", response.text)
        log.info("Status code: %s", response.status_code)

        if response.status_code != 200:
            messages.error(self.request, f"Error starting crawl: {response.text}")
            return super().form_invalid(form)

        obj = response.json()
        # response can be something like:
        # {"status": "error", "message": "spider 'generic_spider' not found"}
        if obj.get('status') == 'error':
            messages.error(self.request, f"Error starting crawl: {obj.get('message')}")
        else:
            messages.info(self.request, f"Crawl of '{start_url}' started")

        return super().form_valid(form)


@require_POST
def start_content_crawl(request, pk):
    """ Starts a content crawl for a certain filter set. """
    filter_set = FilterSet.objects.get(pk=pk)
    start_url = filter_set.crawl_job.start_url
    # follow_links = filter_set.crawl_job.follow_links
    # TODO: a filter set is always linked to a crawl job. Maybe we want to make it so
    # that we can reuse a filter set for multiple jobs?
    parameters = {
        'project': 'scraper',
        'spider': 'generic_spider',
        'filter_set_id': str(pk),
    }

    url = settings.SCRAPYD_URL + "/schedule.json"
    try:
        response = requests.post(url, data=parameters, timeout=5)
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error starting content crawl: {e}")
        return redirect('filter_details', pk=pk)
    print(response.status_code)
    print(response.text)

    if response.status_code != 200:
        messages.error(request, f"Error starting content crawl: {response.text}")
    else:
        obj = response.json()
        # response can be something like:
        # {"status": "error", "message": "spider 'generic_spider' not found"}
        if obj.get('status') == 'error':
            messages.error(request, f"Error starting content crawl: {obj.get('message')}")
        else:
            messages.info(request, f"Content crawl of '{start_url}' started")

    # redirect back to the filter set detail page
    return redirect('filter_details', pk=pk)

