""" Views for the crawls app. """
# pylint: disable=too-many-ancestors

import json
import logging
import os
import threading
import time
from typing import Any, Optional

import redis
import requests
from aggregator import CallbackAggregator
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_not_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, FormView, ListView
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from crawls.fields_processor import FieldsProcessor
from crawls.forms import StartCrawlForm
from crawls.models import Crawler, CrawlJob, FilterRule, FilterSet, SourceItem
from crawls.serializers import (CrawlerSerializer, FilterRuleSerializer,
                                FilterSetSerializer, SourceItemSerializer, CrawlJobSerializer)

log = logging.getLogger(__name__)


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
@login_not_required
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

        # Send initial hello event, so it doesn't show as disconnected in the client
        hello_data = {
            'type': 'hello',
            'message': 'Hello from server',
            'timestamp': time.time()
        }
        yield f"data: {json.dumps(hello_data)}\n\n".encode('utf-8')

        def send_event(event_data):
            event_queue.append(f"data: {json.dumps(event_data)}\n\n".encode('utf-8'))
   
        try:
            aggregator = CallbackAggregator(
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


class CrawlJobViewSet(viewsets.ModelViewSet):
    """ Provides the API under /api/crawl_jobs/ """
    queryset = CrawlJob.objects.all()
    serializer_class = CrawlJobSerializer
    # TODO: restrict to authenticated users!
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['post'])
    def evaluate_filters(self, request, pk=None):
        """ Evaluate the filter set for this crawl job. Lives at
            http://127.0.0.1:8000/api/crawl_jobs/1/evaluate_filters/ """
        
        try:
            crawl_job = self.get_object()
            filter_set = crawl_job.crawler.filter_set
        except ObjectDoesNotExist as e:
            return Response({'error': str(e)}, status=400)
        response_dict = filter_set.evaluate(crawl_job)
        return Response(response_dict)


class FilterSetViewSet(viewsets.ModelViewSet):
    """ Provides the API under /api/filter_sets/ """
    queryset = FilterSet.objects.all()
    serializer_class = FilterSetSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def unmatched(self, request, pk=None):
        """ Returns a list of unmatched URLs. Lives at
            http://127.0.0.1:8000/api/filter_sets/1/unmatched/?crawl_job=<crawl_job_id> """

        crawl_job_id = request.query_params.get("crawl_job")
        if crawl_job_id is None:
            return Response({'error': 'crawl_job parameter is required'}, status=400)
        
        crawl_job = get_object_or_404(CrawlJob, pk=crawl_job_id)

        # pylint: disable=unused-argument
        qs = crawl_job.crawled_urls
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
    permission_classes = [permissions.AllowAny]

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).order_by('position')

    # run code when a new rule is created
    def perform_create(self, serializer: FilterRuleSerializer):  # type: ignore[override]
        """ Run when a new rule is created. """
        rule = serializer.save()
        # rule.filter_set.evaluate()
        # TODO: in what is returned in the request, the new count is not reflected yet (?)
        rule.save()  # ?

    def perform_update(self, serializer: FilterRuleSerializer):  # type: ignore[override]
        """ Run when a rule is updated. """
        log.info("perform_update")
        rule = serializer.save()
        # rule.filter_set.evaluate(rule)
        log.info("Rule %r updated", rule)
        # rule.save()

    # add endpoint under filter_rules/<id>/matches?crawl_job=<crawl_job_id> to get all matching URLs
    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        """ Returns a list of URLs that match this rule. Lives at
            http://127.0.0.1:8000/api/filter_rules/1/matches/ """

        # pylint: disable=unused-argument
        rule = self.get_object()

        crawl_job_id = request.query_params.get("crawl_job")
        if crawl_job_id is None:
            return Response({'error': 'crawl_job parameter is required'}, status=400)
        
        crawl_job = get_object_or_404(CrawlJob, pk=crawl_job_id)

        # get previous rules, when sorted by position
        previous_rules = rule.filter_set.rules.filter(
            position__lt=rule.position)

        # get all URLs that match this rule and any of the previous rules
        qs = crawl_job.crawled_urls
        for r in previous_rules:
            qs = qs.exclude(url__startswith=r.rule)
        new_matches = qs.filter(url__startswith=rule.rule)
        other_matches = crawl_job.crawled_urls.filter(
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

