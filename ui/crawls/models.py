from django.db import models

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