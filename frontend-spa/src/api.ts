import { Crawler, CrawlJob, SourceItem } from "./apitypes";
import { GroupInfo, WloFieldInfo } from "./wloTypes";

export default class Api {
    constructor(private baseUrl: string) {
    }

    // Crawlers

    async listCrawlers(): Promise<Crawler[]> {
        const response = await fetch(`${this.baseUrl}/crawlers/`);
        if (!response.ok) {
            throw new Error(`Failed to fetch crawlers: ${response.status} ${response.statusText}`);
        }
        const data: Crawler[] = await response.json();
        return data;
    }

    async createCrawler(sourceItemGuid: string, startURL: string, crawlerName: string): Promise<Crawler> {
        const response = await fetch(`${this.baseUrl}/crawlers/`, {
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

    async updateCrawler(crawlerId: number, updates: Partial<Crawler>): Promise<Crawler> {
        const response = await fetch(`${this.baseUrl}/crawlers/${crawlerId}/`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(updates)
        });

        if (!response.ok) {
            throw new Error(`Failed to update crawler with ID ${crawlerId}: ${response.status} ${response.statusText}`);
        }

        const data: Crawler = await response.json();
        return data;
    }

    async deleteCrawler(crawlerId: number): Promise<void> {
        const response = await fetch(`${this.baseUrl}/crawlers/${crawlerId}/`, {
            method: "DELETE",
        });
        if (!response.ok) {
            throw new Error(`Failed to delete crawler with ID ${crawlerId}`);
        }
    }

    async startCrawl(crawlerId: number): Promise<CrawlJob> {
        const response = await fetch(`${this.baseUrl}/crawlers/${crawlerId}/start_crawl/`, {
            method: "POST",
        });
        if (!response.ok) {
            throw new Error(`Failed to start crawl for crawler with ID ${crawlerId}`);
        }
        return response.json();
    }

    // TODO: check return type
    async startContentCrawl(crawlerId: number): Promise<CrawlJob> {
        const response = await fetch(`${this.baseUrl}/crawlers/${crawlerId}/start_content_crawl/`, {
            method: "POST",
        });
        if (!response.ok) {
            throw new Error(`Failed to start content crawl for crawler with ID ${crawlerId}`);
        }
        return response.json();
    }

    // Crawl Jobs

    async cancelCrawlJob(crawlJobId: number): Promise<void> {
        const response = await fetch(`${this.baseUrl}/crawl_jobs/${crawlJobId}/cancel/`, {
            method: "POST",
        });
        if (!response.ok) {
            throw new Error(`Failed to cancel crawl job with ID ${crawlJobId}`);
        }
    }

    async deleteCrawlJob(crawlJobId: number): Promise<void> {
        const response = await fetch(`${this.baseUrl}/crawl_jobs/${crawlJobId}/`, {
            method: "DELETE",
        });
        if (!response.ok) {
            throw new Error(`Failed to delete crawl job with ID ${crawlJobId}`);
        }
    }

    // Misc

    getAdminUrl(crawlerId: number): string {
        return `${this.baseUrl.replace('/api', '')}/admin/crawls/crawler/${crawlerId}/change/`;
    }

    // Edu-sharing source items
    
    async listSourceItems(): Promise<SourceItem[]> {
        const response = await fetch(`${this.baseUrl}/source_items/`);
        if (!response.ok) {
            throw new Error(`Failed to fetch source items: ${response.status} ${response.statusText}`);
        }
        const data: SourceItem[] = await response.json();
        return data;
    }

    async getSourceItem(guid: string): Promise<SourceItem> {
        const response = await fetch(`${this.baseUrl}/source_items/${guid}/`);
        if (!response.ok) {
            throw new Error(`Failed to fetch source item ${guid}: ${response.status} ${response.statusText}`);
        }
        return response.json();
    }

    // TODO: check return type
    async getInheritableFields(sourceItemGuid: string): Promise<{fields: WloFieldInfo[]; groups: GroupInfo[]}> {
        const response = await fetch(`${this.baseUrl}/source_items/${sourceItemGuid}/inheritable_fields`);
        if (!response.ok) {
            throw new Error(`Failed to fetch inheritable fields for source item ${sourceItemGuid}: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        return data;
    }

}