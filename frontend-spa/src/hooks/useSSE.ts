import { useEffect, useRef, useState } from 'react';
import { CrawlJobState } from '../apitypes';

export type SSEData = {
    type: 'crawl_job_update';
    crawler_id: number;
    crawl_job: {
        id: number;
        state: CrawlJobState;
        crawled_url_count: number;
    };
    items_processed: number;
    current_url: string;
    timestamp: number;
};

export type SSEError = {
    type: 'error';
    message: string;
    timestamp: number;
};

export type SSEEvent = SSEData | SSEError;

export function useSSE(url: string | null) {
  const [data, setData] = useState<SSEEvent | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!url) return;

    const connectSSE = () => {
      try {
        const eventSource = new EventSource(url);
        eventSourceRef.current = eventSource;

        eventSource.onopen = () => {
          // console.log('SSE connection opened');
          setIsConnected(true);
          setError(null);
        };

        eventSource.onmessage = (event) => {
          try {
            const parsedData: SSEData = JSON.parse(event.data);
            // console.log('SSE data received:', parsedData);
            setData(parsedData);
          } catch (parseError) {
            console.error('Error parsing SSE data:', parseError);
            setError('Failed to parse server data');
          }
        };

        eventSource.onerror = (err) => {
          console.error('SSE error:', err);
          console.error('EventSource readyState:', eventSource.readyState);
          console.error('URL:', url);
          setIsConnected(false);
          
          // Set error message based on readyState
          if (eventSource.readyState === EventSource.CLOSED) {
            setError('Connection closed by server');
          } else if (eventSource.readyState === EventSource.CONNECTING) {
            setError('Connection failed - server unreachable');
          }
          
          // Automatically reconnect after a delay
          setTimeout(() => {
            if (eventSource.readyState === EventSource.CLOSED) {
              // console.log('Attempting to reconnect SSE...');
              connectSSE();
            }
          }, 3000);
        };

      } catch (err) {
        console.error('Error creating EventSource:', err);
        setError('Failed to connect to server');
        setIsConnected(false);
      }
    };

    connectSSE();

    // Cleanup function
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
      setIsConnected(false);
    };
  }, [url]);

  return {
    data,
    error,
    isConnected,
    close: () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null;
        setIsConnected(false);
      }
    }
  };
}

export function useCrawlerSSE(crawlerId: number | string | undefined | null) {
  // Use relative URL to avoid CORS issues during development
  const url = crawlerId ? `http://localhost:8000/api/crawlers/${crawlerId}/status_stream/` : null;
  return useSSE(url);
}