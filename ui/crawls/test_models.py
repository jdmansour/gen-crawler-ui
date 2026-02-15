import pytest
from crawls.models import Crawler, CrawlJob


@pytest.fixture(name='crawler')
def fixture_crawler(db):
    return Crawler.objects.create(
        name="Test Crawler",
        start_url="https://example.com",
        source_item="test-guid",
    )


def make_job(crawler, crawl_type, state):
    return CrawlJob.objects.create(
        crawler=crawler,
        start_url=crawler.start_url,
        crawl_type=crawl_type,
        state=state,
    )


@pytest.mark.django_db
class TestCrawlerState:
    def test_no_jobs_returns_exploration_required(self, crawler):
        assert crawler.state() == Crawler.State.EXPLORATION_REQUIRED

    def test_pending_exploration_returns_exploration_running(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.PENDING)
        assert crawler.state() == Crawler.State.EXPLORATION_RUNNING

    def test_running_exploration_returns_exploration_running(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.RUNNING)
        assert crawler.state() == Crawler.State.EXPLORATION_RUNNING

    def test_failed_exploration_returns_exploration_required(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.FAILED)
        assert crawler.state() == Crawler.State.EXPLORATION_REQUIRED

    def test_completed_exploration_returns_ready_for_content(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.COMPLETED)
        assert crawler.state() == Crawler.State.READY_FOR_CONTENT_CRAWL

    def test_canceled_exploration_returns_ready_for_content(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.CANCELED)
        assert crawler.state() == Crawler.State.READY_FOR_CONTENT_CRAWL

    def test_pending_content_crawl_returns_content_running(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.COMPLETED)
        make_job(crawler, CrawlJob.CrawlType.CONTENT, CrawlJob.State.PENDING)
        assert crawler.state() == Crawler.State.CONTENT_CRAWL_RUNNING

    def test_running_content_crawl_returns_content_running(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.COMPLETED)
        make_job(crawler, CrawlJob.CrawlType.CONTENT, CrawlJob.State.RUNNING)
        assert crawler.state() == Crawler.State.CONTENT_CRAWL_RUNNING

    def test_completed_content_crawl_returns_ready_for_content(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.COMPLETED)
        make_job(crawler, CrawlJob.CrawlType.CONTENT, CrawlJob.State.COMPLETED)
        assert crawler.state() == Crawler.State.READY_FOR_CONTENT_CRAWL

    def test_exploration_running_takes_priority_over_content(self, crawler):
        """If exploration is running, that state wins even if content jobs exist."""
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.RUNNING)
        make_job(crawler, CrawlJob.CrawlType.CONTENT, CrawlJob.State.COMPLETED)
        assert crawler.state() == Crawler.State.EXPLORATION_RUNNING
