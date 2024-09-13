import logging
from typing import Any

import requests
from crawls.models import FilterRule, FilterSet
from crawls.serializers import FilterRuleSerializer, FilterSetSerializer
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .forms import StartCrawlForm
from .models import CrawlJob

log = logging.getLogger(__name__)

class FilterSetViewSet(viewsets.ModelViewSet):
    queryset = FilterSet.objects.all()
    serializer_class = FilterSetSerializer

    # Get a list of URLs that don't match any rule
    @action(detail=True, methods=['get'])
    def unmatched(self, request, pk=None):
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
    queryset = FilterRule.objects.all()
    serializer_class = FilterRuleSerializer

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).order_by('position')

    # run code when a new rule is created
    def perform_create(self, serializer: FilterRuleSerializer):
        rule = serializer.save()
        rule.filter_set.evaluate()
        # TODO: in what is returned in the request, the new count is not reflected yet (?)
        rule.save()  # ?

    def perform_update(self, serializer: FilterRuleSerializer):
        log.info("perform_update")
        rule = serializer.save()
        rule.filter_set.evaluate(rule)
        log.info("Rule %r updated", rule)
        #rule.save()

    # add endpoint under filter_rules/<id>/matches to get all matching URLs
    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        rule = self.get_object()
        # get previous rules, when sorted by position
        previous_rules = rule.filter_set.rules.filter(position__lt=rule.position)
        # get all URLs that match this rule and any of the previous rules
        qs = rule.filter_set.crawl_job.crawled_urls
        for r in previous_rules:
            qs = qs.exclude(url__startswith=r.rule)
        new_matches = qs.filter(url__startswith=rule.rule)
        other_matches = rule.filter_set.crawl_job.crawled_urls.filter(url__startswith=rule.rule).exclude(pk__in=new_matches)
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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context
    
class CrawlDetailView(DetailView):
    model = CrawlJob
    template_name = 'crawl_detail.html'
    context_object_name = 'crawl'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context
    
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
    #success_url = '/crawls/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_success_url(self) -> str:
        # return the new filter set's detail page
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
        url = "http://127.0.0.1:6800/schedule.json"
        response = requests.post(url, data=parameters, timeout=2)

        if response.status_code != 200:
            messages.error(self.request, f"Error starting crawl: {response.text}")
            return super().form_invalid(form)

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

    url = "http://127.0.0.1:6800/schedule.json"
    try:
        response = requests.post(url, data=parameters, timeout=2)
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
