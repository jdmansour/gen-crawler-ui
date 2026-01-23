import os
import redis
import time
import json


def main():
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    redis_client = redis.from_url(redis_url)

    crawler_id = 1
    crawl_job_id = 1
    crawl_job_state = 'RUNNING'
    channel = f'crawler_status_{crawler_id}'

    print("Sending fake updates to channel:", channel)
    maximum = 300
    for i in range(maximum):
        crawl_job_crawled_url_count = (i+1)# * 10
        items_processed = crawl_job_crawled_url_count
        print(f"Sending update {i+1}/{maximum} with fake crawled_url_count={crawl_job_crawled_url_count}")

        status_data = {
            'type': 'crawl_job_update',
            'crawler_id': crawler_id,
            'crawl_job': {
                'id': crawl_job_id,
                'state': crawl_job_state,
                'crawled_url_count': crawl_job_crawled_url_count,
            },
            'items_processed': items_processed,
            'current_url': None,
            'timestamp': time.time()
        }
        redis_client.publish(channel, json.dumps(status_data))
        time.sleep(0.01)

    status_data = {
        'type': 'crawl_job_update',
        'crawler_id': crawler_id,
        'crawl_job': {
            'id': crawl_job_id,
            'state': 'COMPLETED',
            'crawled_url_count': maximum,
        },
        'items_processed': maximum,
        'current_url': None,
        'timestamp': time.time()
    }
    redis_client.publish(channel, json.dumps(status_data))

if __name__ == '__main__':
    main()