import { GroupInfo, WloFieldInfo } from "./wloTypes";

export type CrawlJobState = 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';

export type Crawler = {
    id: number;
    url: string;
    filter_set_id: number | null;
    filter_set_url: string | null;
    name: string;
    status: CrawlerStatus;
    created_at: string;
    updated_at: string;
    source_item: string;
    start_url: string;
    inherited_fields: string[];
    crawl_jobs: CrawlJob[];
};

export type CrawlerStatus = "draft" |
  "pending" |
  "stopped" |
  "error" |
  "published";
    
export type SourceItem = {
    id: number;
    guid: string;
    title: string;
    created_at: string;
    updated_at: string;
    data: any;

    preview_url: string;
};

export type CrawlJob = {
    id: number;
    start_url: string;
    follow_links: boolean;
    created_at: string;
    updated_at: string;
    state: CrawlJobState;
    crawled_url_count: number;
    scrapy_job_id: string | null;
    crawler: number;
}


export async function createCrawler(sourceItemGuid: string, startURL: string, crawlerName: string): Promise<Crawler> {
    const response = await fetch("http://localhost:8000/api/crawlers/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            source_item: sourceItemGuid,
            start_url: startURL,
            name: crawlerName,
        })
    });

    if (!response.ok) {
        throw new Error(`Failed to create crawler: ${response.status} ${response.statusText}`);
    }

    const data: Crawler = await response.json();
    return data;
}
    
export async function getInheritableFields(sourceItemGuid: string): Promise<{fields: WloFieldInfo[]; groups: GroupInfo[]}> {
    const response = await fetch(`http://localhost:8000/api/source_items/${sourceItemGuid}/inheritable_fields`);
    const data = await response.json();
    return data;
}
export type RuleEvaluation = {
  id: number;
  rule: string;
  include: boolean;
  created_at: string;
  updated_at: string;
  page_type: string;
  count: number;
  cumulative_count: number;
  position: number;
};
export type EvaluateFiltersResult = {
  id: number;
  remaining_urls: number;
  name: string;
  created_at: string;
  updated_at: string;
  rules: RuleEvaluation[];
};
