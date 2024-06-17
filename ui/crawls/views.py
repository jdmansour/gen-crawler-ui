from crawls.serializers import FilterSetSerializer, FilterRuleSerializer
from crawls.models import FilterRule, FilterSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import logging
log = logging.getLogger(__name__)

class FilterSetViewSet(viewsets.ModelViewSet):
    queryset = FilterSet.objects.all()
    serializer_class = FilterSetSerializer


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
    
