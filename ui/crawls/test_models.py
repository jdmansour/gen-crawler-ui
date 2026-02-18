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

    def test_failed_exploration_returns_exploration_required_job_failed(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.FAILED)
        assert crawler.state() == Crawler.State.EXPLORATION_REQUIRED_JOB_FAILED

    def test_completed_exploration_returns_ready_for_content(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.COMPLETED)
        assert crawler.state() == Crawler.State.READY_FOR_CONTENT_CRAWL

    def test_canceled_exploration_returns_ready_for_content(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.CANCELED)
        assert crawler.state() == Crawler.State.READY_FOR_CONTENT_CRAWL

    def test_failed_then_completed_exploration_returns_ready_for_content(self, crawler):
        """A completed exploration after a failed one means we're past exploration."""
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.FAILED)
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.COMPLETED)
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

    def test_failed_content_crawl_returns_job_failed(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.COMPLETED)
        make_job(crawler, CrawlJob.CrawlType.CONTENT, CrawlJob.State.FAILED)
        assert crawler.state() == Crawler.State.READY_FOR_CONTENT_CRAWL_JOB_FAILED

    def test_completed_then_failed_content_crawl_returns_job_failed(self, crawler):
        """Latest content job failed, even though a previous one succeeded."""
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.COMPLETED)
        make_job(crawler, CrawlJob.CrawlType.CONTENT, CrawlJob.State.COMPLETED)
        make_job(crawler, CrawlJob.CrawlType.CONTENT, CrawlJob.State.FAILED)
        assert crawler.state() == Crawler.State.READY_FOR_CONTENT_CRAWL_JOB_FAILED

    def test_failed_then_completed_content_crawl_clears_error(self, crawler):
        """A successful content crawl after a failure clears the error state."""
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.COMPLETED)
        make_job(crawler, CrawlJob.CrawlType.CONTENT, CrawlJob.State.FAILED)
        make_job(crawler, CrawlJob.CrawlType.CONTENT, CrawlJob.State.COMPLETED)
        assert crawler.state() == Crawler.State.READY_FOR_CONTENT_CRAWL

    def test_exploration_running_takes_priority_over_content(self, crawler):
        """If exploration is running, that state wins even if content jobs exist."""
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.RUNNING)
        make_job(crawler, CrawlJob.CrawlType.CONTENT, CrawlJob.State.COMPLETED)
        assert crawler.state() == Crawler.State.EXPLORATION_RUNNING


@pytest.mark.django_db
class TestCrawlerSimpleState:
    def test_no_jobs_returns_draft(self, crawler):
        assert crawler.simple_state() == 'draft'

    def test_exploration_running_returns_running(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.RUNNING)
        assert crawler.simple_state() == 'running'

    def test_ready_for_content_returns_idle(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.COMPLETED)
        assert crawler.simple_state() == 'idle'

    def test_content_running_returns_running(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.COMPLETED)
        make_job(crawler, CrawlJob.CrawlType.CONTENT, CrawlJob.State.RUNNING)
        assert crawler.simple_state() == 'running'

    def test_exploration_failed_returns_error(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.FAILED)
        assert crawler.simple_state() == 'error'

    def test_content_failed_returns_error(self, crawler):
        make_job(crawler, CrawlJob.CrawlType.EXPLORATION, CrawlJob.State.COMPLETED)
        make_job(crawler, CrawlJob.CrawlType.CONTENT, CrawlJob.State.FAILED)
        assert crawler.simple_state() == 'error'
