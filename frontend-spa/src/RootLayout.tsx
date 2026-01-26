// RootLayout.tsx
import { createTheme, ThemeProvider } from "@mui/material";
import { useCallback, useEffect, useState } from "react";
import { Outlet, useNavigate, useParams } from "react-router-dom";
import { Crawler, CrawlJob, SourceItem } from "./apitypes";
import Breadcrumbs, { Breadcrumb } from "./Breadcrumbs";
import GenCrawlerSidebar from "./GenCrawlerSidebar";
import { RootContext } from "./RootContext";
import SiteLayout, { ShowSidebarButton } from "./SiteLayout";
import { CrawlerDashboardStep } from "./steps";
import { wloThemeData } from "./wloTheme";
import WloFakeHeader from "./WloFakeHeader";
import { SSEData } from "./hooks/useSSE";
import {ApiUrlContext, useApiUrl} from "./ApiUrlContext.tsx";
import Api from "./api.ts";

export default function RootLayout() {
  const apiUrl = useApiUrl();
  const [sidebarVisible, setSidebarVisible] = useState(true);

  const [crawlerList, setCrawlerList] = useState<Crawler[]>([]);
  const [crawlerListLoaded, setCrawlerListLoaded] = useState<boolean>(false);
  // select source
  const [sourceItems, setSourceItems] = useState<SourceItem[]>([]);
  const [selectedSourceItem, setSelectedSourceItem] = useState<SourceItem | null>(null);



  const [step, setStep] = useState<CrawlerDashboardStep>("dashboard");
  const params = useParams();
  const crawlerId : number | undefined = params.crawlerId ? parseInt(params.crawlerId) : undefined;

  const navigate = useNavigate();
  function setHistoryState(state: {
    step: CrawlerDashboardStep;
    newCrawlerName?: string;
  }) {
    const loc = "/" + state.step;
    navigate(loc, { state: state, replace: false });
  }

  const api = new Api("http://localhost:8000/api");

  // State manangement
  // -----------------
  function onCrawlJobAdded(newJob: CrawlJob) {
      const crawlerId = newJob.crawler;
      setCrawlerList(crawlerList => crawlerList.map(c => c.id === crawlerId ? { ...c, crawl_jobs: [newJob, ...c.crawl_jobs] } : c));
  }

  function onCrawlJobDeleted(crawlJobId: number) {
      const crawlerId = crawlerList.find(c => c.crawl_jobs.some(j => j.id === crawlJobId))?.id;
      if (!crawlerId) {
          console.error(`Crawl job with ID ${crawlJobId} not found in any crawler.`);
          return;
      }
      setCrawlerList(crawlerList => crawlerList.map(c => c.id === crawlerId ? { ...c, crawl_jobs: c.crawl_jobs.filter(j => j.id !== crawlJobId) } : c));
  }

  const onCrawlJobLiveUpdate = useCallback((sseData: SSEData) => {
      setCrawlerList(crawlerList => crawlerList.map(c => mergeCrawler(c, sseData)));
  }, [setCrawlerList]);

  function onCrawlerDeleted(crawlerId: number) {
      setCrawlerList(crawlerList => crawlerList.filter(c => c.id !== crawlerId));
  }

  // Delete a crawler and update state
  async function deleteCrawler(crawlerId: number) {
    await api.deleteCrawler(crawlerId);
    onCrawlerDeleted(crawlerId);
    navigate("/");
  }

  async function startSearchCrawl(crawlerId: number) {
    const crawlJob = await api.startCrawl(crawlerId);
    onCrawlJobAdded(crawlJob);
    return crawlJob;
  }

  async function startContentCrawl(crawlerId: number) {
    const crawlJob = await api.startContentCrawl(crawlerId);
    // todo: update state
    return crawlJob;
  }

  const outletContext: RootContext = {
    sourceItems: sourceItems,
    setStep: setStep,
    onSourceSelected: (source: SourceItem) => {
      setSelectedSourceItem(source);
      setHistoryState({ step: "add-crawler", newCrawlerName: "abcd" });
    },
    setSidebarVisible,
    onCrawlJobAdded,
    onCrawlJobDeleted,
    onCrawlJobLiveUpdate,
    onCrawlerDeleted,
    crawlerList: crawlerList,
    setCrawlerList: setCrawlerList,
    crawlerListLoaded,
    deleteCrawler,
    startSearchCrawl,
    startContentCrawl,
    sourceItem: selectedSourceItem || undefined,
    setSourceItem: setSelectedSourceItem,
  };

  const breadcrumbs: Breadcrumb[] = [
    { label: "Startseite", url: "/" },
    { label: "Quellen", url: "/" },
    { label: "Generischer Crawler", url: "/" },
  ];
  if (step == "select-source") {
    breadcrumbs.push({ label: "Quelle auswählen", temporary: true });
  } else if (step == "add-crawler") {
    breadcrumbs.push({ label: "Crawler Details", temporary: true });
  } else if (step == "metadata-inheritance" || step == "filter-crawls" || step == "crawler-details") {
    const crawlerName = crawlerList.find(c => c.id == crawlerId)?.name;
    breadcrumbs.push({ label: crawlerName || "-", url: `/crawlers/${crawlerId}` });
  }

  async function fetchCrawlers() {
    const response = await fetch(apiUrl + "/crawlers/");
    const data: Crawler[] = await response.json();
    // TODO: validate?
    // wait 2 seconds to simulate loading
    await new Promise((resolve) => setTimeout(resolve, 2000));
    setCrawlerList(data);
    setCrawlerListLoaded(true);
  }

  async function fetchSourceItems() {
    const response = await fetch(apiUrl + "/source_items/");
    const data: SourceItem[] = await response.json();
    setSourceItems(data);
  }

  useEffect(() => {
    fetchCrawlers();
    fetchSourceItems();
  }, []);

  const wloTheme = createTheme(wloThemeData);

  return (
    <ThemeProvider theme={wloTheme}>
    <div style={{ display: "flex", flexDirection: "column", flex: "1" }} >
      <SiteLayout
        style={{ }}
        sidebar={<GenCrawlerSidebar step={step} />}
        sidebarVisible={sidebarVisible}
        onSidebarClose={() => setSidebarVisible(false)} >
        {!sidebarVisible && (
          <ShowSidebarButton onClick={() => setSidebarVisible(true)} />
        )}

        <Breadcrumbs breadcrumbs={breadcrumbs} />
        <Outlet context={outletContext} />
      </SiteLayout>
      {/* <footer>WLO Footer here</footer> */}
    </div>
    </ThemeProvider>
  );
}

function mergeCrawlJob(job: CrawlJob, update: Partial<CrawlJob>): CrawlJob {
    if (job.id != update.id) return job;
    return { ...job, ...update };
}
function mergeCrawler(c: Crawler, sseData: SSEData): Crawler {
    if (c.id != sseData.crawler_id) return c;
    return { ...c,
            crawl_jobs: c.crawl_jobs.map(job => mergeCrawlJob(job, sseData.crawl_job)) };
}