""" Defines all our models. """

from __future__ import annotations

import logging

from django.db import models

log = logging.getLogger(__name__)


class CrawlJob(models.Model):
    """ A crawl job contains a start URL and references to all crawled URLs. """

    id = models.AutoField(primary_key=True)
    start_url = models.URLField()
    follow_links = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    crawled_urls: models.QuerySet[CrawledURL]
    filter_sets: models.QuerySet[FilterSet]

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
    crawl_job = models.ForeignKey(
        CrawlJob, on_delete=models.CASCADE, related_name="filter_sets")
    remaining_urls = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rules: models.QuerySet[FilterRule]

    def __str__(self):
        return self.name

    def evaluate(self, rule=None):
        """ Evaluate the filter set. If a rule is given, evaluate this rule
        and all dependent (later) rules. If no rule is given, evaluate all rules."""

        log.info("Evaluating filter set %s", self.name)
        log.info("Rule: %s", rule)

        # count how many URLs start with rule.rule
        # TODO: rewrite using sqlite GLOB?
        # TODO: start with the given rule and do all after
        rules = self.rules.order_by('position')
        q = self.crawl_job.crawled_urls
        # total_matches = 0
        for r in rules:
            log.info("Evaluating rule %s", r.rule)
            r.count = self.crawl_job.crawled_urls.filter(
                url__startswith=r.rule).count()
            r.cumulative_count = q.filter(url__startswith=r.rule).count()
            log.info("Count: %d in isolation, %d after previous rules",
                     r.count, r.cumulative_count)
            # total_matches += r.cumulative_count
            r.save(update_fields=[
                   'count', 'cumulative_count'], force_update=True)

            # select all that don't trigger the filter
            q = q.exclude(url__startswith=r.rule)
            # cumulative_count = q.count()
            # cumulative_count += r.count
        # self.remaining_urls = self.crawl_job.crawled_urls.count() - total_matches
        self.remaining_urls = q.count()
        log.info("Remaining URLs: %d", self.remaining_urls)
        self.save(update_fields=['remaining_urls'], force_update=True)
        # log.info("Done")
        # return rules


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
        if new_position == self.position:
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
