// RootLayout.tsx
import { Alert, createTheme, Snackbar, ThemeProvider } from "@mui/material";
import { useCallback, useEffect, useState } from "react";
import { Outlet, useNavigate, useParams } from "react-router-dom";
import Api from "./api.ts";
import { Crawler, CrawlJob, SourceItem } from "./apitypes";
import { useApiUrl } from "./ApiUrlContext.tsx";
import Breadcrumbs, { Breadcrumb } from "./Breadcrumbs";
import GenCrawlerSidebar from "./GenCrawlerSidebar";
import { CrawlerUpdate, CrawlJobUpdate, SSEData, useCrawlerSSE } from "./hooks/useSSE";
import { RootContext } from "./RootContext";
import SiteLayout, { ShowSidebarButton } from "./SiteLayout";
import { CrawlerDashboardStep } from "./steps";
import { wloThemeData } from "./wloTheme";

export default function RootLayout() {
  const apiUrl = useApiUrl();
  const [sidebarVisible, setSidebarVisible] = useState(true);

  const [crawlerList, setCrawlerList] = useState<Crawler[]>([]);
  const [crawlerListLoaded, setCrawlerListLoaded] = useState<boolean>(false);
  // select source
  const [sourceItems, setSourceItems] = useState<SourceItem[]>([]);
  const [selectedSourceItem, setSelectedSourceItem] = useState<SourceItem | null>(null);

  const [observedCrawlerId, setObservedCrawlerId] = useState<number | null>(null);


  const [toastMessage, setToastMessage] = useState("");
  const [toastOpen, setToastOpen] = useState(false);
  function showToast(message: string) {
    setToastMessage(message);
    setToastOpen(true);
  }

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

  // update the fields of the crawler matching sseData.crawler_id with the data from
  // sseData (status and timestamp)
  const onCrawlerUpdate = useCallback((sseData: CrawlerUpdate) => {
      console.log("Updating crawler with ID", sseData.crawler_id, "to state", sseData.state);
      const crawlerId = typeof sseData.crawler_id === 'string' ? parseInt(sseData.crawler_id) : sseData.crawler_id;
      setCrawlerList(crawlerList => crawlerList.map(c =>
        (c.id === crawlerId) ? { ...c, state: sseData.state } : c));
  }, [setCrawlerList]);

  const onCrawlJobLiveUpdate = useCallback((sseData: CrawlJobUpdate) => {
      setCrawlerList(crawlerList => crawlerList.map(c => mergeCrawlJobUpdate(c, sseData)));
  }, [setCrawlerList]);

  function onCrawlerDeleted(crawlerId: number) {
      setCrawlerList(crawlerList => crawlerList.filter(c => c.id !== crawlerId));
  }

  // SSE for real-time updates
  const { data: sseData, isConnected, error: sseError } = useCrawlerSSE(observedCrawlerId);

  useEffect(() => {
      if (!sseData) return;

      console.log("SSE data received in RootLayout:", sseData);
      
      switch (sseData.type) {
          case 'crawler_update':
              onCrawlerUpdate(sseData);
              break;

          case 'crawl_job_update':                
              onCrawlJobLiveUpdate(sseData);
              break;
              
          case 'error':
              console.error('SSE Error:', sseData.message);
              break;
      }
  }, [onCrawlJobLiveUpdate, onCrawlerUpdate, sseData]);

  // Delete a crawler and update state
  async function deleteCrawler(crawlerId: number) {
    await api.deleteCrawler(crawlerId);
    onCrawlerDeleted(crawlerId);
    navigate("/");
  }

  async function startSearchCrawl(crawlerId: number) {
    const crawlJob = await api.startCrawl(crawlerId);
    onCrawlJobAdded(crawlJob);
    showToast("Explorations-Crawl wurde gestartet");
    return crawlJob;
  }

  async function startContentCrawl(crawlerId: number) {
    const crawlJob = await api.startContentCrawl(crawlerId);
    console.log("Started content crawl:", crawlJob);
    onCrawlJobAdded(crawlJob);
    showToast("Content-Crawl wurde gestartet");
    return crawlJob;
  }

  async function cancelCrawlJob(crawlJobId: number) {
    await api.cancelCrawlJob(crawlJobId);
    // todo: update state?
  }

  async function deleteCrawlJob(crawlJobId: number) {
    await api.deleteCrawlJob(crawlJobId);
    onCrawlJobDeleted(crawlJobId);
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
    onCrawlerDeleted,
    crawlerList: crawlerList,
    setCrawlerList: setCrawlerList,
    crawlerListLoaded,
    deleteCrawler,
    startSearchCrawl,
    startContentCrawl,
    cancelCrawlJob,
    deleteCrawlJob,
    liveUpdatesConnected: isConnected,
    liveUpdatesError: sseError,
    sourceItem: selectedSourceItem || undefined,
    setSourceItem: setSelectedSourceItem,
    setObservedCrawlerId,
    showToast,
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
  } else if (step == "metadata-inheritance" || step == "filter-crawls" || step == "crawler-details" || step == "filters") {
    const crawlerName = crawlerList.find(c => c.id == crawlerId)?.name;
    breadcrumbs.push({ label: crawlerName || "-", url: `/crawlers/${crawlerId}` });
    if (step == "filters") {
      breadcrumbs.push({ label: "Filterregeln" });
    } else if (step == "metadata-inheritance") {
      breadcrumbs.push({ label: "Metadatenvererbung" });
    }
  }

  useEffect(() => {
    async function fetchCrawlers() {
      const response = await fetch(apiUrl + "/crawlers/");
      const data: Crawler[] = await response.json();
      // TODO: validate?
      // wait 2 seconds to simulate loading
      // await new Promise((resolve) => setTimeout(resolve, 2000));
      setCrawlerList(data);
      setCrawlerListLoaded(true);
    }

    async function fetchSourceItems() {
      const response = await fetch(apiUrl + "/source_items/");
      const data: SourceItem[] = await response.json();
      setSourceItems(data);
    }

    fetchCrawlers();
    fetchSourceItems();
  }, [apiUrl]);

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
      <Snackbar open={toastOpen} autoHideDuration={4000} onClose={() => setToastOpen(false)}>
        <Alert onClose={() => setToastOpen(false)} severity="success" variant="filled">
          {toastMessage}
        </Alert>
      </Snackbar>
    </div>
    </ThemeProvider>
  );
}

function mergeCrawlJob(job: CrawlJob, update: Partial<CrawlJob>): CrawlJob {
    if (job.id != update.id) return job;
    return { ...job, ...update };
}
function mergeCrawlJobUpdate(c: Crawler, sseData: CrawlJobUpdate): Crawler {
    if (c.id != sseData.crawler_id) return c;
    return { ...c,
            crawl_jobs: c.crawl_jobs.map(job => mergeCrawlJob(job, sseData.crawl_job)) };
}