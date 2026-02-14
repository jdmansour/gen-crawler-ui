
import time

from aggregator import CallbackAggregator

def test_last_event_wins():
    """Same event type - only the last event should be kept."""
    received_events = []
    def add_event(event):
        received_events.append(event)
    aggregator = CallbackAggregator(debounce_ms=200, max_wait_ms=600, callback=add_event)
    for i in range(6):
        aggregator.add_event({"type": "status_update", "value": i})
        time.sleep(0.1)
    time.sleep(0.25)
    assert len(received_events) == 1
    assert received_events[0] == {"type": "status_update", "value": 5}
    print("Received events:", received_events)

def test_debounce():
    """Same event type - should be coalesced per debounce window."""
    received_events = []
    def add_event(event):
        received_events.append(event)
    aggregator = CallbackAggregator(debounce_ms=200, max_wait_ms=1000, callback=add_event)

    aggregator.add_event({"type": "status_update", "value": 1})
    time.sleep(0.1)
    aggregator.add_event({"type": "status_update", "value": 2})
    time.sleep(0.1)
    aggregator.add_event({"type": "status_update", "value": 3})
    time.sleep(0.25)  # wait longer than debounce to trigger send
    aggregator.add_event({"type": "status_update", "value": 4})

    time.sleep(0.25)
    assert len(received_events) == 2
    assert received_events == [
        {"type": "status_update", "value": 3},
        {"type": "status_update", "value": 4}
    ]
    print("Received events:", received_events)

def test_regular_events():
    """Same event type - should send out events when max_wait is exceeded."""
    received_events = []
    def add_event(event):
        received_events.append(event)
    aggregator = CallbackAggregator(debounce_ms=200, max_wait_ms=500, callback=add_event)

    for i in range(10):
        aggregator.add_event({"type": "status_update", "value": i})
        time.sleep(0.1)

    time.sleep(0.25)
    assert len(received_events) == 2
    assert received_events == [
        {"type": "status_update", "value": 4},
        {"type": "status_update", "value": 9}
    ]
    print("Received events:", received_events)

def test_different_event_types():
    """Different event types should NOT be merged - each type should produce a separate event."""
    received_events = []
    def add_event(event):
        received_events.append(event)
    aggregator = CallbackAggregator(debounce_ms=200, max_wait_ms=1000, callback=add_event)

    aggregator.add_event({"type": "status_update", "value": 1})
    aggregator.add_event({"type": "progress_update", "progress": 50})
    aggregator.add_event({"type": "status_update", "value": 2})
    aggregator.add_event({"type": "progress_update", "progress": 75})

    time.sleep(0.25)  # wait for debounce

    # Should receive 2 events: one for each type (with the latest value for each)
    assert len(received_events) == 2
    # Events can be in any order, so sort by type for assertion
    received_events.sort(key=lambda e: e["type"])
    assert received_events == [
        {"type": "progress_update", "progress": 75},
        {"type": "status_update", "value": 2}
    ]
    print("Received events:", received_events)

def test_different_crawl_jobs():
    """Different crawl job IDs should NOT be merged - each job should produce a separate event."""
    received_events = []
    def add_event(event):
        received_events.append(event)
    aggregator = CallbackAggregator(debounce_ms=200, max_wait_ms=1000, callback=add_event)

    # Add updates for two different crawl jobs
    aggregator.add_event({"type": "crawl_job_update", "crawl_job": {"id": 1, "status": "running"}})
    aggregator.add_event({"type": "crawl_job_update", "crawl_job": {"id": 2, "status": "running"}})
    aggregator.add_event({"type": "crawl_job_update", "crawl_job": {"id": 1, "status": "completed"}})
    aggregator.add_event({"type": "crawl_job_update", "crawl_job": {"id": 2, "status": "completed"}})

    time.sleep(0.25)  # wait for debounce

    # Should receive 2 events: one for each crawl job (with the latest status for each)
    assert len(received_events) == 2
    # Events can be in any order, so sort by job ID for assertion
    received_events.sort(key=lambda e: e["crawl_job"]["id"])
    assert received_events == [
        {"type": "crawl_job_update", "crawl_job": {"id": 1, "status": "completed"}},
        {"type": "crawl_job_update", "crawl_job": {"id": 2, "status": "completed"}}
    ]
    print("Received events:", received_events)

def test_mixed_events():
    """Mix of different event types and crawl job updates - all should be kept separate."""
    received_events = []
    def add_event(event):
        received_events.append(event)
    aggregator = CallbackAggregator(debounce_ms=200, max_wait_ms=1000, callback=add_event)

    aggregator.add_event({"type": "status_update", "value": 1})
    aggregator.add_event({"type": "crawl_job_update", "crawl_job": {"id": 1, "status": "running"}})
    aggregator.add_event({"type": "crawl_job_update", "crawl_job": {"id": 2, "status": "running"}})
    aggregator.add_event({"type": "status_update", "value": 2})

    time.sleep(0.25)  # wait for debounce

    # Should receive 3 events: 1 status_update + 2 crawl_job_updates
    assert len(received_events) == 3
    # Sort by type then by job ID for consistent ordering
    received_events.sort(key=lambda e: (e["type"], e.get("crawl_job", {}).get("id", 0)))
    assert received_events == [
        {"type": "crawl_job_update", "crawl_job": {"id": 1, "status": "running"}},
        {"type": "crawl_job_update", "crawl_job": {"id": 2, "status": "running"}},
        {"type": "status_update", "value": 2}
    ]
    print("Received events:", received_events)