import { Crawler, SourceItem } from "./apitypes";
import { CrawlerDashboardStep } from "./steps";

export type DashboardPageContext = {
  crawlerList: Crawler[];
  setCrawlerList: (crawlers: Crawler[] | ((prev: Crawler[]) => Crawler[])) => void;
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
  // onCreateClick: (source: SourceItem, crawlerURL: string, crawlerName: string) => void;
  setCrawlerList: (crawlers: Crawler[]) => void;
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
};

export type UseStepContext = {
  setStep: (step: CrawlerDashboardStep) => void;
};

export type RootContext = DashboardPageContext & SelectSourcePageContext & AddCrawlerPageContext & MetadataInheritancePageContext & CrawlerDetailsPageContext & UseStepContext;


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
