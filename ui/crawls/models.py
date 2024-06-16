from django.db import models
import logging
log = logging.getLogger(__name__)


# Create your models here.
class CrawlJob(models.Model):
    id = models.AutoField(primary_key=True)
    start_url = models.URLField()
    follow_links = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.start_url} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    

class CrawledURL(models.Model):
    crawl_job = models.ForeignKey(CrawlJob, on_delete=models.CASCADE)
    url = models.URLField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url
    

class FilterSet(models.Model):
    id = models.AutoField(primary_key=True)
    crawl_job = models.ForeignKey(CrawlJob, on_delete=models.CASCADE, related_name="filter_sets")
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def evaluate(self, rule=None):
        """ Evaluate the filter set. If a rule is given, evaluate this rule
        and all dependent (later) rules. If no rule is given, evaluate all rules."""
        
        log.info(f"Evaluating filter set {self.name}")
        log.info(f"Rule: {rule}")

        # count how many URLs start with rule.rule
        # TODO: rewrite using sqlite GLOB?
        if rule:
            rule.count = CrawledURL.objects.filter(url__startswith=rule.rule).count()
            rule.save()
        else:
            rules = self.rules.all()
            for r in rules:
                r.count = CrawledURL.objects.filter(url__startswith=r.rule).count()
                r.save()
        log.info("Done")
        # return rules


class FilterRule(models.Model):
    filter_set = models.ForeignKey(FilterSet, on_delete=models.CASCADE, related_name="rules")
    rule = models.TextField()
    include = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Later add more metadata?
    page_type = models.CharField(max_length=255, default="")
    # Filled out later by script
    count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.rule
