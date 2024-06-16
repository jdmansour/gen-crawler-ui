from crawls.serializers import FilterSetSerializer, FilterRuleSerializer
from crawls.models import FilterRule, FilterSet
from rest_framework import viewsets

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

    
