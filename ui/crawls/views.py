""" Views for the crawls app. """
# pylint: disable=too-many-ancestors

import json
import logging
import os
import threading
import time

import redis
import requests
from aggregator import CallbackAggregator
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_not_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from crawls.fields_processor import FieldsProcessor
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

    def perform_create(self, serializer) -> None:
        crawler = serializer.save()
        # Create a default FilterSet for this Crawler
        filter_set = FilterSet.objects.create(
            name=crawler.name,
            crawler=crawler,
        )
        filter_set.save()

    @action(detail=True, methods=['post'])
    def start_crawl(self, request, pk=None):
        print("start_crawl called")
        print("pk:", pk)
        obj = self.get_object()
        print("Crawler:", obj)

        # create crawl job object
        crawljob = CrawlJob.objects.create(
            start_url=obj.start_url,
            follow_links=True,
            crawler=obj,
            state='PENDING',
            crawl_type='EXPLORATION',
        )
        crawljob.save()
        print("Created CrawlJob:", crawljob)

        # Start scrapy job
        parameters = {
            'project': 'scraper',
            'spider': 'example',
            'start_url': obj.start_url,
            'follow_links': True,
            'crawler_id': str(obj.id),
            'crawl_job_id': str(crawljob.id),
        }
        # get SCRAPYD_URL from settings
        url = settings.SCRAPYD_URL + "/schedule.json"
        response = requests.post(url, data=parameters, timeout=5)
        log.info("Response: %s", response.text)
        log.info("Status code: %s", response.status_code)
        if response.status_code != 200:
            # update crawljob state to ERROR
            crawljob.state = 'ERROR'
            crawljob.save()
            return Response({'status': 'error', 'message': response.text}, status=500)

        crawljob.scrapy_job_id = response.json().get('jobid', '')
        crawljob.save()

        serializer = CrawlJobSerializer(crawljob)
        return Response(serializer.data)

        
    @action(detail=True, methods=['post'])
    def start_content_crawl(self, request, pk=None):
        """ Starts a content crawl for this crawler's filter set. Lives at
            http://127.0.0.1:8000/api/crawlers/<pk>/start_content_crawl/ """
        crawler = self.get_object()

        # create crawl job object
        crawljob = CrawlJob.objects.create(
            start_url=crawler.start_url,  # not used in content crawl
            follow_links=True,  # not used in content crawl
            crawler=crawler,
            state='PENDING',
            crawl_type='CONTENT',
        )
        crawljob.save()
        print("Created CrawlJob:", crawljob)

        parameters = {
            'project': 'scraper',
            'spider': 'generic_spider',
            'filter_set_id': str(crawler.filter_set.id),
            'crawler_id': str(crawler.id),
            'crawl_job_id': str(crawljob.id),
        }

        ## TODO: implement the other path in generic_spider.py where we start a crawl and pass filter_set_id!!!

        url = settings.SCRAPYD_URL + "/schedule.json"
        response = requests.post(url, data=parameters, timeout=5)
        log.info("Response: %s", response.text)
        log.info("Status code: %s", response.status_code)
        if response.status_code != 200:
            crawljob.state = 'ERROR'
            crawljob.save()
            return Response({'status': 'error', 'message': response.text}, status=500)
        # Respone is like:
        # {"node_name": "8cc425300b18", "status": "ok", "jobid": "03d1f0d8fb8211f0aff70242ac120004"}
        # Set the correct scrapy_job_id on the crawljob, so the frontend can refer to it
        crawljob.scrapy_job_id = response.json().get('jobid', '')
        crawljob.save()

        serializer = CrawlJobSerializer(crawljob)
        return Response(serializer.data)


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
                # Always use a short timeout so we regularly check event_queue
                # for events delivered by the aggregator's timer thread.
                # Using timeout=None would block indefinitely in parse_response,
                # preventing us from yielding aggregated events from event_queue.
                message = pubsub.handle_message(pubsub.parse_response(timeout=0.5, block=False))  # type: ignore

                # Yield all queued events from the aggregator
                while event_queue:
                    event = event_queue.pop(0)
                    yield event

                if message is None:
                    continue

                if message['type'] != 'message':
                    continue

                try:
                    data = json.loads(message['data'].decode('utf-8'))
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
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """ Cancel this crawl job. Lives at
            http://127.0.0.1:8000/api/crawl_jobs/1/cancel/ """
        
        scrapy_job_id = self.get_object().scrapy_job_id
        if not scrapy_job_id:
            message = f"Crawl job {pk} has no scrapy_job_id, cannot cancel."
            return Response({'status': 'error', 'message': message}, status=400)
        
        url = settings.SCRAPYD_URL + "/cancel.json"
        parameters = {
            'project': 'scraper',
            'job': scrapy_job_id,
        }
        response = requests.post(url, data=parameters, timeout=5)
        log.info("Response: %s", response.text)
        log.info("Status code: %s", response.status_code)
        if response.status_code != 200:
            return Response({'status': 'error', 'message': response.text}, status=500)

        obj = response.json()
        return Response(obj)


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
        # limit to 30 results each
        new_matches = new_matches.all()[:30]
        other_matches = other_matches.all()[:30]
        result = {
            'new_matches': [url.url for url in new_matches],
            'other_matches': [url.url for url in other_matches],
        }

        # matches = rule.filter_set.crawl_job.crawled_urls.filter(url__startswith=rule.rule)
        # result = {
        #     'matches': [url.url for url in matches],
        # }
        return Response(result)


class HealthViewSet(viewsets.ViewSet):
    """ Provides the API under /api/health/ """

    permission_classes = [permissions.AllowAny]

    def list(self, request):
        """ Return health status. """
        return Response({'status': 'ok'})

