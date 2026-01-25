import { CrawlJob } from "./apitypes";

export default class Api {
    constructor(private baseUrl: string) {
    }

    // Crawlers

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

}