
export type CrawlerDashboardStep =
  | "dashboard"
  | "select-source"
  | "metadata-inheritance"
  | "filter-crawls";
export class CrawlerInfo {
  id: number;
  name: string;
  status: CrawlerStatus;
  updatedAt: Date;
  constructor(
    id: number,
    name: string,
    status: CrawlerStatus,
    updatedAt: Date,
  ) {
    this.id = id;
    this.name = name;
    this.status = status;
    this.updatedAt = updatedAt;
  }
}

export type CrawlerStatus = "draft" |
  "pending" |
  "stopped" |
  "error" |
  "published";
