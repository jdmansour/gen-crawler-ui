export type CrawlerResponse = {
    id: number;
    name: string;
    // status: CrawlerStatus;
    created_at: string;
    updated_at: string;
    source_item: string;
};

export type SourceItem = {
    id: number;
    guid: string;
    title: string;
    created_at: string;
    updated_at: string;
    data: any;

    preview_url: string;
};



export async function createCrawler(sourceItemGuid: string, startURL: string, crawlerName: string): Promise<CrawlerResponse> {
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

    const data: CrawlerResponse = await response.json();
    return data;
}
    
