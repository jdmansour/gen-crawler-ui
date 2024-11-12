
Some useful SQL queries:

Find duplicate URLs:

```sql
SELECT url, crawl_job_id, COUNT(crawl_job_id)
FROM crawls_crawledurl
WHERE url LIKE "%de/service%" AND crawl_job_id = 28
GROUP BY url, crawl_job_id
LIMIT 100
```

or

```sql
SELECT url, crawl_job_id, COUNT(crawl_job_id) AS  c
FROM crawls_crawledurl
WHERE crawl_job_id = 28
GROUP BY url, crawl_job_id HAVING c > 1
LIMIT 1000
```

or

```sql
SELECT *
FROM crawls_crawledurl
WHERE crawl_job_id = 28 AND rowid NOT IN
(
	SELECT min(rowid)
	FROM crawls_crawledurl
	GROUP BY url, crawl_job_id 
)
```

Delete the duplicates (dangerous):

```sql
DELETE
FROM crawls_crawledurl
WHERE crawl_job_id = 28 AND rowid NOT IN
(
	SELECT min(rowid)
	FROM crawls_crawledurl
	GROUP BY url, crawl_job_id 
)
```