""" Views for the crawls app. """
# pylint: disable=too-many-ancestors

import json
import logging
from typing import Any, Optional

import requests
from crawls.forms import StartCrawlForm
from crawls.models import Crawler, CrawlJob, FilterRule, FilterSet, SourceItem
from crawls.serializers import (CrawlerSerializer, FilterRuleSerializer,
                                FilterSetSerializer, SourceItemSerializer)
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, FormView, ListView
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

log = logging.getLogger(__name__)

class SourceItemViewSet(viewsets.ModelViewSet):
    """ Provides the API under /api/source_items/ """
    queryset = SourceItem.objects.all()
    serializer_class = SourceItemSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'guid'

    @action(detail=True, methods=['get'])
    def inheritable_fields(self, request, guid=None):
        """ Returns a list of inheritable fields for this source item. Lives at
            http://127.0.0.1:8000/api/source_items/<guid>/inheritable_fields/ """
        
        # for now, return contents of data/inheritable_fields.json
        with open('data/inheritable_fields.json', 'r', encoding='utf-8') as f:
            fields = json.load(f)
        return Response(fields)


class CrawlerViewSet(viewsets.ModelViewSet):
    """ Provides the API under /api/crawlers/ """
    queryset = Crawler.objects.all()
    serializer_class = CrawlerSerializer
    # TODO: restrict to authenticated users!
    permission_classes = [permissions.AllowAny]

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
