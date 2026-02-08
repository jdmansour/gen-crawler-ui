""" Serializers define the API representation. """
from __future__ import annotations
from rest_framework import serializers
from crawls.models import Crawler, FilterRule, FilterSet, CrawlJob, SourceItem


class SourceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceItem
        fields = ['id', 'guid', 'title', 'created_at', 'updated_at', 'data', 'preview_url']
        read_only_fields = ['created_at', 'updated_at', 'preview_url']


class CrawlJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlJob
        fields = '__all__'

    crawled_url_count = serializers.SerializerMethodField('get_crawled_url_count')

    def get_crawled_url_count(self, obj: CrawlJob):
        return obj.crawled_urls.count()


class CrawlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crawler
        fields = ['id', 'url', 'filter_set_id', 'filter_set_url', 'name', 'start_url', 'source_item',
                  'created_at', 'updated_at', 'inherited_fields', 'state', 'crawl_jobs']
        read_only_fields = ['id', 'created_at', 'updated_at', 'state', 'crawl_jobs']
        depth = 1

    crawl_jobs = CrawlJobSerializer(many=True, read_only=True)
    filter_set_id = serializers.ReadOnlyField(source='filter_set.id')
    filter_set_url = serializers.HyperlinkedRelatedField(
        view_name='filterset-detail', read_only=True, source='filter_set')
    

class FilterRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FilterRule
        fields = ['id', 'filter_set', 'rule', 'include', 'created_at',
                  'updated_at', 'page_type', 'count', 'cumulative_count', 'position']

    # serialize, but don't deserialize count
    count = serializers.ReadOnlyField()
    cumulative_count = serializers.ReadOnlyField()

    # if position is updated, call move_to on the FilterRule
    def update(self, instance, validated_data):
        if 'count' in validated_data:
            validated_data.pop('count')
        if '+' in validated_data:
            instance.move_to(validated_data['position'])
            validated_data.pop('position')
        return super().update(instance, validated_data)


class InlineFilterRuleSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer for FilterRule, omits the urls of the rule and the set. """
    class Meta:
        model = FilterRule
        fields = ['id', 'rule', 'include', 'created_at', 'updated_at',
                  'page_type', 'count', 'cumulative_count', 'position']


class FilterSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterSet
        fields = ['id', 'url', 'crawler_id', 'crawler_url', 'remaining_urls', 'name',
                  'created_at', 'updated_at', 'rules']
        depth = 1

    # order rules by position, ascending
    rules = serializers.SerializerMethodField('get_rules')
    crawler_url = serializers.HyperlinkedRelatedField(
        view_name='crawler-detail', read_only=True, source='crawler')

    def get_rules(self, obj):
        rules = obj.rules.order_by('position')
        return InlineFilterRuleSerializer(rules, many=True, context=self.context).data
