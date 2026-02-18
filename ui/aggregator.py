
# Event aggreator
# - If an event comes in, wait for X ms to see if more events come in
# - If more events come in, reset the timer
# - If no more events come in within X ms, send the aggregated event
# - If the total wait time exceeds Y ms, send the aggregated event anyway and reset the timers
# - Never swallow an event at the end

import threading
import logging
log = logging.getLogger(__name__)

class BaseAggregator:
    def __init__(self, debounce_ms=200, max_wait_ms=1000):
        log.info("BaseAggregator init: debounce_ms=%d, max_wait_ms=%d", debounce_ms, max_wait_ms)
        self.debounce_ms = debounce_ms
        self.max_wait_ms = max_wait_ms
        self.events = []
        self.timer = None
        self.max_wait_timer = None
        # protect self.events with a lock
        self.lock = threading.Lock()
    
    def add_event(self, event):
        # self.last_event_time = time.time()
        with self.lock:
            self.events.append(event)

        # make sure the timers are running
        if not self.timer or not self.timer.is_alive():
            self._start_timer()
        else:
            # reset the debounce timer
            self.timer.cancel()
            self._start_timer()
        if not self.max_wait_timer or not self.max_wait_timer.is_alive():
            self._start_max_wait_timer()

    def _start_timer(self):
        with self.lock:
            #assert self.timer is None or not self.timer.is_alive()
            if self.timer and self.timer.is_alive():
                self.timer.cancel()
            # random debounce ms up til self.debounce_ms
            # debounce_delay = int(self.debounce_ms * random.uniform(0, 1))
            # self.timer = threading.Timer(debounce_delay / 1000.0, self._debounce_callback)
            self.timer = threading.Timer(self.debounce_ms / 1000.0, self._debounce_callback)
            self.timer.start()
    
    def _start_max_wait_timer(self):
        with self.lock:
            assert self.max_wait_timer is None or not self.max_wait_timer.is_alive()
            self.max_wait_timer = threading.Timer(self.max_wait_ms / 1000.0, self._max_wait_callback)
            self.max_wait_timer.start()

    def _ensure_max_wait_timer(self):
        with self.lock:
            if not self.max_wait_timer or not self.max_wait_timer.is_alive():
                self.max_wait_timer = threading.Timer(self.max_wait_ms / 1000.0, self._max_wait_callback)
                self.max_wait_timer.start()

    def _debounce_callback(self):
        log.info("_debounce_callback")
        self._send_event()

    def _max_wait_callback(self):
        log.info("_max_wait_callback")
        # send event anyway, and schedule another max wait timer
        self._send_event(due_to_max_wait=True)
        self._ensure_max_wait_timer()

    def _send_event(self, due_to_max_wait=False):
        log.info("_send_event called, due_to_max_wait=%s", due_to_max_wait)
        with self.lock:
            if not self.events:
                log.info("  No events to send")
                return
            coalesced = self.coalesce_events(self.events)
            self.events = []
            if self.timer and self.timer.is_alive():
                self.timer.cancel()
            if self.max_wait_timer and self.max_wait_timer.is_alive():
                self.max_wait_timer.cancel()
        for event in coalesced:
            log.info("  Sending coalesced event: %s", event)
            self.send_event(event)

        #self.timer = None


    def send_event(self, event):
        raise NotImplementedError("send_event must be implemented by subclasses")

    def coalesce_events(self, events):
        """Return a list of coalesced events. Must be implemented by subclasses."""
        raise NotImplementedError("coalesce_events must be implemented by subclasses")


class CallbackAggregator(BaseAggregator):
    def __init__(self, debounce_ms=200, max_wait_ms=1000, callback=None):
        super().__init__(debounce_ms, max_wait_ms)
        self.callback = callback

    def send_event(self, event):
        print("Sending event:", event)
        if self.callback:
            self.callback(event)

    def coalesce_events(self, events):
        """Coalesce events, keeping the latest event per unique key.

        For crawl_job_update events, the key is the crawl_job id (so updates
        for different jobs are never dropped). For other event types, the key
        is just the type string. This ensures we deduplicate frequent updates
        for the *same* job while never silently dropping updates for a
        different job.
        """
        if not events:
            return []
        # Keep last event per unique key, preserving insertion order
        merged = {}
        for event in events:
            if event.get('type') == 'crawl_job_update':
                key = ('crawl_job_update', event.get('crawl_job', {}).get('id'))
            else:
                key = (event.get('type'),)
            merged[key] = event
        return list(merged.values())
