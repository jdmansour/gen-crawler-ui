import { Crawler, CrawlJob, SourceItem } from "./apitypes";
import { CrawlerDashboardStep } from "./steps";

export type DashboardPageContext = {
  crawlerList: Crawler[];
  setCrawlerList: (crawlers: Crawler[] | ((prev: Crawler[]) => Crawler[])) => void;
  setSidebarVisible: (visible: boolean) => void;
  setObservedCrawlerId: (crawlerId: number | null) => void;
  crawlerListLoaded: boolean;
};

export type SelectSourcePageContext = {
  sourceItems: SourceItem[];
  onSourceSelected: (source: SourceItem) => void;
};

export type AddCrawlerPageContext = {
  sourceItem?: SourceItem;
  setSourceItem: (source: SourceItem) => void;
  crawlerList: Crawler[];
  sourceItems: SourceItem[];
  setCrawlerList: (crawlers: Crawler[]) => void;
  startSearchCrawl: (crawlerId: number) => Promise<CrawlJob>;
  showToast: (message: string) => void;
};

export type MetadataInheritancePageContext = {
  crawlerList: Crawler[];
  // fields: WloFieldInfo[];
  // groups: GroupInfo[];
};

export type CrawlerDetailsPageContext = {
  sourceItems: SourceItem[];
  crawlerList: Crawler[];
  setCrawlerList: (crawlers: Crawler[] | ((prev: Crawler[]) => Crawler[])) => void;
  onCrawlJobAdded: (newJob: CrawlJob) => void;
  onCrawlerDeleted: (crawlerId: number) => void;
};

export type CrawlerDetailsContext = {
  deleteCrawler: (crawlerId: number) => Promise<void>;
  startSearchCrawl: (crawlerId: number) => Promise<CrawlJob>;
  startContentCrawl: (crawlerId: number) => Promise<CrawlJob>;
  cancelCrawlJob: (crawlJobId: number) => Promise<void>;
  deleteCrawlJob: (crawlJobId: number) => Promise<void>;
  setObservedCrawlerId: (crawlerId: number | null) => void;
  liveUpdatesConnected: boolean;
  liveUpdatesError: string | null;
  crawlerListLoaded: boolean;
};

export type UseStepContext = {
  setStep: (step: CrawlerDashboardStep) => void;
};

export type ToastContext = {
  showToast: (message: string) => void;
};

export type FilterSetPageContext = {
  crawlerList: Crawler[];
  crawlerListLoaded: boolean;
};

export type RootContext =
  DashboardPageContext &
  SelectSourcePageContext &
  AddCrawlerPageContext &
  MetadataInheritancePageContext &
  CrawlerDetailsPageContext &
  CrawlerDetailsContext &
  UseStepContext &
  FilterSetPageContext &
  ToastContext;


// export type RootContext = {
//   sourceItems: SourceItem[];
//   onCancelClick?: () => void;
//   onSourceSelected?: (source: SourceItem) => void;
//   setStep: (step: CrawlerDashboardStep) => void;
//   crawlerList: CrawlerResponse[];
//   onCrawlerClick?: (crawlerId: number) => void;
//   onNewCrawlerClick?: () => void;

//   sourceItem?: SourceItem;
//   // onCancelClick?: () => void;
//   onCreateClick?: (source: SourceItem, crawlerURL: string, crawlerName: string) => void;

//     // metadatainheritance props
//     fields: WloFieldInfo[];
//     groups: GroupInfo[];
//     onSave?: (selectedFields: Record<string, boolean>) => void;
// };
