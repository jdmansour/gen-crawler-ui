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