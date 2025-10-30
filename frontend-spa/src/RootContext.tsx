import { SourceItem } from "./apitypes";
import { CrawlerDashboardStep, CrawlerInfo } from "./types";
import { GroupInfo, WloFieldInfo } from "./wloTypes";

export type DashboardPageContext = {
  crawlerList: CrawlerInfo[];
  setCrawlerName: (name: string|null) => void;
};

export type SelectSourcePageContext = {
  sourceItems: SourceItem[];
  onSourceSelected: (source: SourceItem) => void;
};

export type AddCrawlerPageContext = {
  sourceItem?: SourceItem;
  onCreateClick: (source: SourceItem, crawlerURL: string, crawlerName: string) => void;
};

export type MetadataInheritancePageContext = {
  fields: WloFieldInfo[];
  groups: GroupInfo[];
  onSave: (selectedFields: Record<string, boolean>) => void;
};

export type CrawlerDetailsPageContext = {
  crawlerList: CrawlerInfo[];
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
//   crawlerList: CrawlerInfo[];
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
