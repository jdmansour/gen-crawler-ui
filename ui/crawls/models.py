""" Defines all our models. """

from __future__ import annotations

import logging

from django.db import models

log = logging.getLogger(__name__)

## WLO Sources

class SourceItem(models.Model):
    """ An edu-sharing source item that can be crawled. """

    id = models.AutoField(primary_key=True)
    guid = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = models.JSONField()
    # cclom:general_description
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.title} ({self.guid})"

    def preview_url(self) -> str:
        """ Returns the preview URL for this source item. """
        return self.data.get('preview', {}).get('url', None)

## Crawlers

class Crawler(models.Model):
    """ A definition of a generic web crawler. """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # This could be multiple URLs in the future
    start_url = models.URLField()
    # The source item in edu-sharing as a GUID
    source_item = models.CharField(max_length=255)
    # TODO: add validation
    # List of field IDs that are inherited from the source item
    inherited_fields = models.JSONField(default=list)

    def __str__(self):
        return self.name
    
    class State(models.TextChoices):
        EXPLORATION_REQUIRED = 'EXPLORATION_REQUIRED', 'Exploration Required'
        EXPLORATION_RUNNING = 'EXPLORATION_RUNNING', 'Exploration Running'
        READY_FOR_CONTENT_CRAWL = 'READY_FOR_CONTENT_CRAWL', 'Ready for Content Crawl'
        CONTENT_CRAWL_RUNNING = 'CONTENT_CRAWL_RUNNING', 'Content Crawl Running'

    # TODO: recalculate this when a dynamic update of a crawl job is sent to the client.
    # Where do we do that best?
    def state(self) -> str:
        """ Returns the current state of the crawler based on its crawl jobs. """
        crawl_jobs = self.crawl_jobs.all()
        if crawl_jobs.filter(crawl_type=CrawlJob.CrawlType.EXPLORATION, state__in=[CrawlJob.State.RUNNING, CrawlJob.State.PENDING]).exists():
            return self.State.EXPLORATION_RUNNING
        elif not crawl_jobs.filter(crawl_type=CrawlJob.CrawlType.EXPLORATION, state__in=[CrawlJob.State.COMPLETED, CrawlJob.State.CANCELED]).exists():
            return self.State.EXPLORATION_REQUIRED
        elif crawl_jobs.filter(crawl_type=CrawlJob.CrawlType.CONTENT, state__in=[CrawlJob.State.RUNNING, CrawlJob.State.PENDING]).exists():
            return self.State.CONTENT_CRAWL_RUNNING
        else:
            return self.State.READY_FOR_CONTENT_CRAWL

class CrawlJob(models.Model):
    """ A crawl job contains a start URL and references to all crawled URLs. """

    # Crawl job state: pending, running, completed, failed, canceled
    class State(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        RUNNING = 'RUNNING', 'Running'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
        CANCELED = 'CANCELED', 'Canceled'

    class CrawlType(models.TextChoices):
        EXPLORATION = 'EXPLORATION', 'Exploration'
        CONTENT = 'CONTENT', 'Content'

    id = models.AutoField(primary_key=True)
    start_url = models.URLField()
    follow_links = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    crawled_urls: models.QuerySet[CrawledURL]
    filter_sets: models.QuerySet[FilterSet]
    crawler = models.ForeignKey(
        Crawler, on_delete=models.CASCADE, related_name="crawl_jobs")
    state = models.CharField(
        max_length=20, choices=State.choices, default=State.PENDING)
    scrapy_job_id = models.CharField(max_length=255, blank=True, null=True)
    crawl_type = models.CharField(
        max_length=20, choices=CrawlType.choices, default=CrawlType.EXPLORATION)

    def __str__(self):
        return f"#{self.id} {self.start_url} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class CrawledURLIndexManager(models.Manager):
    """ Custom manager for the CrawledURL model. """

    def get_queryset(self):
        return super().get_queryset().filter(noindex=False)

class CrawledURL(models.Model):
    """ A URL that has been crawled by our scraper. """

    crawl_job = models.ForeignKey(
        CrawlJob, on_delete=models.CASCADE, related_name="crawled_urls")
    url = models.URLField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    noindex = models.BooleanField(default=False)

    objects = CrawledURLIndexManager()
    all_objects = models.Manager()

    # make crawl_job_id and url unique together
    class Meta:
        unique_together = ('crawl_job', 'url')

    def __str__(self):
        return self.url


class FilterSet(models.Model):
    """ A set of rules that can be used to filter URLs in a crawl job. """

    id = models.AutoField(primary_key=True)

    # TODO: FilterSets should now attach to Crawlers, not CrawlJobs
    # Each Crawler has exactly one FilterSet (one on one)
    crawler = models.OneToOneField(
        Crawler, on_delete=models.CASCADE, related_name="filter_set", blank=True, null=True)
    remaining_urls = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rules: models.QuerySet[FilterRule]

    def __str__(self):
        return self.name

    def evaluate(self, crawl_job: CrawlJob, rule=None):
        """ Evaluate the filter set. If a rule is given, evaluate this rule
        and all dependent (later) rules. If no rule is given, evaluate all rules."""

        log.info("Evaluating filter set %s", self.name)
        log.info("Rule: %s", rule)

        # count how many URLs start with rule.rule
        # TODO: rewrite using sqlite GLOB?
        # TODO: start with the given rule and do all after
        rules = self.rules.order_by('position')
        q = crawl_job.crawled_urls
        # total_matches = 0
        # rule_id -> {rule, count, cumulative_count}
        results = []
        for r in rules:
            log.info("Evaluating rule %s on CrawlJob %s", r.rule, crawl_job.id)
            count = crawl_job.crawled_urls.filter(
                url__startswith=r.rule).count()
            cumulative_count = q.filter(url__startswith=r.rule).count()
            log.info("Count: %d in isolation, %d after previous rules",
                     count, cumulative_count)
            
            results.append({
                'id': r.pk,
                'rule': r.rule,
                'include': r.include,
                'created_at': r.created_at,
                'updated_at': r.updated_at,
                'page_type': r.page_type,
                'count': count,
                'cumulative_count': cumulative_count,
                'position': r.position
            })

            # r.save(update_fields=[
            #        'count', 'cumulative_count'], force_update=True)

            # select all that don't trigger the filter
            q = q.exclude(url__startswith=r.rule)

        remaining_urls = q.count()
        log.info("Remaining URLs: %d", remaining_urls)
        return {
            'id': self.id,
            'remaining_urls': remaining_urls,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'rules': results
        }
    
    def fix_rule_positions(self):
        """ Fix the positions of the rules in this filter set. """
        # Get a list of all positions and ids, ordered by position ascending.
        # If a position is duplicate, the rules will be ordered arbitrarily (by id).
        # Then, go through the list and reassign positions to be 1, 2, 3, ... in the order of the list.
        rules = self.rules.order_by('position', 'id')
        for i, rule in enumerate(rules):
            if rule.position != i + 1:
                log.info("Fixing position of rule %s from %d to %d",
                         rule.rule, rule.position, i + 1)
                rule.position = i + 1
                rule.save(update_fields=['position'], force_update=True)        

class FilterRule(models.Model):
    """ A rule to filter URLs in or out. """

    filter_set = models.ForeignKey(
        FilterSet, on_delete=models.CASCADE, related_name="rules")
    rule = models.TextField()
    include = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    position = models.IntegerField(default=0)
    # Later add more metadata?
    page_type = models.CharField(max_length=255, default="")
    # Filled out later by script
    count = models.IntegerField(default=0)
    cumulative_count = models.IntegerField(default=0)

    def __repr__(self):
        return (f"FilterRule({self.rule}, {self.include}, {self.position}, "
                f"{self.count}, {self.cumulative_count})")

    # on creation, set position to the highest position in the set
    def save(self, *args, **kwargs):
        if not self.position:
            # set to max + 1
            current_max = self.filter_set.rules.aggregate(
                models.Max('position'))['position__max']
            if current_max is None:
                current_max = 0
            self.position = current_max + 1
        super().save(*args, **kwargs)

    def move_to(self, new_position: int):
        """ Move the rule to the new position. If the position is already taken,
            increase the position of all rules above the new position by 1. """
        # TODO: We have to renumber the rules when one is deleted.
        log.info("move_to called with new_position %d for rule %s at position %d",
                 new_position, self.rule, self.position)
        if new_position == self.position:
            # check for duplicates at this position and fix them
            if self.filter_set.rules.filter(position=self.position).count() > 1:
                log.info("Duplicate positions found for position %d, fixing positions", self.position)
                self.filter_set.fix_rule_positions()
            return
        new_position = clamp(new_position, 1, self.filter_set.rules.count())
        log.info("Moving rule %s from %d to %d",
                 self.rule, self.position, new_position)
        if new_position > self.position:
            # move down
            rules = self.filter_set.rules.filter(
                position__gt=self.position, position__lte=new_position)
            log.info("Moving down rules: %s", [r.position for r in rules])
            for r in rules:
                r.position -= 1
                r.save()
        else:
            # move up
            rules = self.filter_set.rules.filter(
                position__gte=new_position, position__lt=self.position)
            log.info("Moving up rules: %s", [r.position for r in rules])
            for r in rules:
                r.position += 1
                r.save()
        self.position = new_position
        self.save()

    def __str__(self):
        return self.rule


def clamp(n, smallest, largest):
    """ Ensures a number is between smallest and largest (inclusive). """

    return max(smallest, min(n, largest))
