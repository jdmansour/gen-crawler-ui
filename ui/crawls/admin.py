""" Admin interface for the crawls app. """

from __future__ import annotations

import logging
from typing import Any

from django import forms
from django.contrib import admin
from django.contrib.admin import display
from django.db import models
from django.db.models import Count, OuterRef, QuerySet, Subquery, Value
from django.forms import TextInput
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from .admin_utils import ReverseModelChoiceField
from .models import (CrawledURL, Crawler, CrawlJob, FilterRule, FilterSet,
                     SourceItem)

log = logging.getLogger(__name__)

class SourceItemAdmin(admin.ModelAdmin):
    model = SourceItem
    list_display = ['title', 'guid', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


class CrawlJobInline(admin.TabularInline):
    model = CrawlJob
    extra = 0
    fields = ['pk', 'crawl_type_display', 'start_url', 'follow_links', 'created_at', 'updated_at']
    readonly_fields = [
        'pk', 'crawl_type_display', 'start_url', 'follow_links', 'created_at', 'updated_at']
    can_delete = False
    show_change_link = True

    @display(description='Type')
    def crawl_type_display(self, obj: CrawlJob) -> str:
        if obj.crawl_type == CrawlJob.CrawlType.EXPLORATION:
            return '🧭 Exploration'
        return '🪄 Content'


class FilterSetInline(admin.TabularInline):
    model = FilterSet
    extra = 0
    fields = ['pk', 'created_at', 'updated_at']
    readonly_fields = ['pk', 'created_at', 'updated_at']
    can_delete = False
    show_change_link = True


class CrawlerAdminForm(forms.ModelForm):
    filter_set = ReverseModelChoiceField(
        queryset=FilterSet.objects.all(),
        required=False,
        help_text="The FilterSet associated with this Crawler.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["filter_set"].initial = getattr(self.instance, "filter_set", None)

    def clean_filter_set(self):
        filter_set = self.cleaned_data.get("filter_set")
        if filter_set and filter_set.crawler is not None and filter_set.crawler != self.instance:
            raise forms.ValidationError(
                f"FilterSet '{filter_set}' is already used by crawler '{filter_set.crawler}'. "
                "Each FilterSet can only be associated with one crawler."
            )
        return filter_set

    def save(self, commit=True):
        instance = super().save(commit)
        filter_set = self.cleaned_data.get("filter_set")
        self.fields["filter_set"].save_related(self.instance, filter_set) # pyright: ignore[reportAttributeAccessIssue]

        return instance


class CrawlerAdmin(admin.ModelAdmin):
    model = Crawler
    list_display = ['name', 'start_url', 'source_item',
                    'created_at', 'updated_at', 'inherited_fields']
    fields = ['name', 'start_url', 'source_item',
              'inherited_fields', 'created_at', 'updated_at',
              'filter_set'
              ]
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CrawlJobInline, FilterSetInline]

    form = CrawlerAdminForm

                         


class FilterRuleInline(admin.TabularInline):
    model = FilterRule
    extra = 0
    fields = ['pk', 'id', 'rule', 'created_at', 'updated_at',
              'position', 'count', 'cumulative_count']
    readonly_fields = ['pk', 'id', 'created_at',
                       'updated_at', 'position', 'count', 'cumulative_count']
    # make rule a single line input field
    formfield_overrides = {
        models.TextField: {'widget': TextInput(attrs={'size': '40'})},
    }
    can_delete = False
    show_change_link = True
    ordering = ['position']


class FilterSetAdmin(admin.ModelAdmin):
    model = FilterSet
    list_display = ['name', 'crawler_link',
                    'created_at', 'updated_at', 'rules_count']
    readonly_fields = ['remaining_urls', 'created_at', 'updated_at']
    inlines = [FilterRuleInline]

    # @mark_safe
    # @display(description='Crawl Job')
    # def crawl_lob_link(self, obj: FilterSet) -> str:
    #     return f'<a href="/admin/crawls/crawljob/{obj.crawl_job.id}/">{obj.crawl_job}</a>'

    @mark_safe
    @display(description='Crawler')
    def crawler_link(self, obj: FilterSet) -> str:
        if obj.crawler is None:
            return 'No Crawler'
        return f'<a href="/admin/crawls/crawler/{obj.crawler.id}/">{obj.crawler}</a>'

    @display(description='# Rules')
    def rules_count(self, obj: FilterSet) -> int:
        return obj.rules.count()

    def save_related(self, request: Any, form: Any, formsets: Any, change: Any) -> None:
        """ Called after saving the main object and related objects.
            This is used to recompute the filter set after saving the rules. """

        super().save_related(request, form, formsets, change)
        for formset in formsets:
            # check if this formset is for FilterRule
            if formset.model == FilterRule:
                formset.save(commit=False)
                # instances = formset.save(commit=False)
                # for instance in instances:
                #     instance.filter_set.evaluate()
                #     break


class CrawlJobAdmin(admin.ModelAdmin):
    list_display = ['start_url', 'crawl_type', 'follow_links', 'created_at',
                    'updated_at', 'crawled_urls_count']
    fields = ['start_url', 'crawl_type', 'follow_links',
              'created_at', 'updated_at', 'crawled_urls', 'crawler', 'scrapy_job_id']
    readonly_fields = ['created_at', 'crawl_type', 'follow_links', 'updated_at', 'crawled_urls', 'crawler']
    date_hierarchy = 'created_at'

    class AnnotatedCrawlJob(CrawlJob):
        """ CrawlJob with additional fields we fetch in get_queryset(). """
        crawled_urls_count: int
        # filter_sets_count: int

    # link to the admin page for the related crawled urls
    @mark_safe
    def crawled_urls(self, obj: AnnotatedCrawlJob) -> str:
        try:
            count = obj.crawled_urls_count
            if count == 0:
                return 'No crawled URLs'
            return f'<a href="/admin/crawls/crawledurl/?crawl_job__id__exact={obj.id}">{count} Crawled URLs</a>'
        except AttributeError as e:
            print("Error in crawled_urls", e)
            return 'Error'

    @display(description='# Crawled URLs')
    def crawled_urls_count(self, obj: AnnotatedCrawlJob) -> int:
        print("crawled_urls, obj is", type(obj))
        return obj.crawled_urls_count

    @display(description='# Filter Sets')
    def filter_sets_count(self, obj: AnnotatedCrawlJob) -> int:
        return obj.filter_sets_count # pyright: ignore[reportAttributeAccessIssue]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = super().get_queryset(request)

        # We are constructing a query like this:
        #
        # SELECT id, start_url,
        # (
        #     SELECT COUNT(*)
        #     FROM crawls_crawledurl
        #     WHERE crawls_crawljob.id = crawls_crawledurl.crawl_job_id
        # ) AS url_count
        # FROM crawls_crawljob

        crawled_urls_count_subquery = (
            CrawledURL.objects.filter(crawl_job=OuterRef('pk'))
            # dummy to get rid of the GROUP BY
            .annotate(d=Value(1)).values('d')
            .annotate(c=Count('*')).values('c')
        )
        # filter_sets_count_subquery = (
        #     FilterSet.objects.filter(crawl_job=OuterRef('pk'))
        #     # dummy to get rid of the GROUP BY
        #     .annotate(d=Value(1)).values('d')
        #     .annotate(c=Count('*')).values('c')
        # )
        queryset = queryset.annotate(
            crawled_urls_count=Subquery(crawled_urls_count_subquery),
            # filter_sets_count=Subquery(filter_sets_count_subquery),
        )

        # This would also work, but the above is much faster
        # (2 ms vs 3000 ms).  The reason is that django uses this
        # queryset to display the date hierarchy widget.  When
        # using subqueries, it drops the unneeded 'count' columns,
        # but when using JOIN, it keeps the join and fetches
        # unneccessarily many rows.

        # queryset = queryset.select_related().annotate(
        #     crawled_urls_count=Count('crawled_urls__pk', distinct=True),
        #     # filter_sets_count=Count('filter_sets', distinct=True),
        # )

        return queryset

    # make this model read only
    # type: ignore[override]
    # def has_change_permission(self, request: HttpRequest, obj: Optional[CrawlJob] = None) -> bool:
    #     return False
        # return super().has_change_permission(request, obj)


class CrawlJobFilter(admin.SimpleListFilter):
    title = 'Crawl Job'
    parameter_name = 'crawl_job__id__exact'

    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin) -> list:
        job_id = self.value()

        if job_id:
            job = CrawlJob.objects.get(id=job_id)
            description = f"Job {job_id}: {job.start_url} at {job.created_at}"
            return [
                (job_id, description),
            ]
        return []
        # return [
        #     (job.id, job.start_url) for job in crawl_jobs
        # ]
        # if job_id:
        #     return [(job.id, job.start_url) for job in crawl_jobs if job.id == int(job_id)]
        # return [(job.id, job.start_url) for job in crawl_jobs]

    def queryset(self, request: HttpRequest, queryset):
        if self.value():
            return queryset.filter(crawl_job__id=self.value())
        return queryset
    # def __init__(self, field, request, params, model, model_admin, field_path):
    #     self.lookup_kwarg = "%s__in" % field_path
    #     super().__init__(field, request, params, model, model_admin, field_path)

    # def expected_parameters(self):
    #     return [self.lookup_kwarg]

    # def choices(self, changelist):
    #     return []


class CrawledURLAdmin(admin.ModelAdmin):
    model = CrawledURL
    list_display = ['url','index', 'crawl_job', 'created_at', 'updated_at']
    # fields = ['url', 'crawl_job', 'content', 'created_at', 'updated_at']
    # readonly_fields = ['url', 'crawl_job', 'content', 'created_at', 'updated_at']
    # date_hierarchy = 'created_at'

    # allow to filter by crawl job
    # list_filter = [(CrawlJobFilter)]
    list_filter = ['crawl_job']

    @display(description='do index', boolean=True)
    def index(self, obj: CrawledURL) -> bool:
        return not obj.noindex


admin.site.register(SourceItem, SourceItemAdmin)
admin.site.register(Crawler, CrawlerAdmin)
admin.site.register(CrawlJob, CrawlJobAdmin)
admin.site.register(CrawledURL, CrawledURLAdmin)
admin.site.register(FilterSet, FilterSetAdmin)
