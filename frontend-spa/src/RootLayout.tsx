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

export default function RootLayout() {
  const [sidebarVisible, setSidebarVisible] = useState(true);

  const [crawlerList, setCrawlerList] = useState<Crawler[]>([]);
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


  const outletContext: RootContext = {
    sourceItems: sourceItems,
    setStep: setStep,
    onSourceSelected: (source: SourceItem) => {
      setSelectedSourceItem(source);
      setHistoryState({ step: "add-crawler", newCrawlerName: "abcd" });
    },
    onCrawlJobAdded,
    onCrawlJobDeleted,
    onCrawlJobLiveUpdate,
    onCrawlerDeleted,
    crawlerList: crawlerList,
    setCrawlerList: setCrawlerList,
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
    const response = await fetch("http://localhost:8000/api/crawlers/");
    const data: Crawler[] = await response.json();
    // TODO: validate?
    setCrawlerList(data);
  }

  async function fetchSourceItems() {
    const response = await fetch("http://localhost:8000/api/source_items/");
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
    <div style={{ display: "flex", flexDirection: "column", height: "100vh" }} >
      <WloFakeHeader />
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