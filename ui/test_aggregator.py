
import time

from aggregator import CallbackAggregator

def test_last_event_wins():
    received_events = []
    def add_event(event):
        received_events.append(event)
    aggregator = CallbackAggregator(debounce_ms=200, max_wait_ms=600, callback=add_event)
    for i in range(6):
        aggregator.add_event(f"event {i}")
        time.sleep(0.1)
    time.sleep(0.25)
    assert len(received_events) == 1
    assert received_events[0] == "event 5"
    print("Received events:", received_events)

def test_debounce():
    received_events = []
    def add_event(event):
        received_events.append(event)
    aggregator = CallbackAggregator(debounce_ms=200, max_wait_ms=1000, callback=add_event)

    aggregator.add_event("event 1")
    time.sleep(0.1)
    aggregator.add_event("event 2")
    time.sleep(0.1)
    aggregator.add_event("event 3")
    time.sleep(0.25)  # wait longer than debounce to trigger send
    aggregator.add_event("event 4")

    time.sleep(0.25)
    assert len(received_events) == 2
    assert received_events == ["event 3", "event 4"]
    print("Received events:", received_events)

def test_regular_events():
    # It should send out the event in the middle, even though it is blocked by debounce
    received_events = []
    def add_event(event):
        received_events.append(event)
    aggregator = CallbackAggregator(debounce_ms=200, max_wait_ms=500, callback=add_event)

    for i in range(10):
        aggregator.add_event(f"event {i}")
        time.sleep(0.1)

    time.sleep(0.25)
    assert len(received_events) == 2
    assert received_events == ["event 4", "event 9"]
    print("Received events:", received_events)