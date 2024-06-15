
export type Rule = {
  id: number;
  rule: string;
  count: number;
  include: boolean;
  page_type: string;
};

export type CrawlJob = {
  id: number;
  start_url: string;
  follow_links: boolean;
  created_at: string;
  updated_at: string;
};

export type FilterSet = {
  id: number
  crawl_job: CrawlJob
  name: string
  created_at: string
  updated_at: string
  url: string
  rules: Rule[]
}

