// RootLayout.tsx
import { useEffect, useState } from "react";
import { Outlet, useNavigate, useParams } from "react-router-dom";
import { Crawler, SourceItem } from "./apitypes";
import Breadcrumbs, { Breadcrumb } from "./Breadcrumbs";
import GenCrawlerSidebar from "./GenCrawlerSidebar";
import { RootContext } from "./RootContext";
import SiteLayout, { ShowSidebarButton } from "./SiteLayout";
import { CrawlerDashboardStep } from "./steps";
import { createTheme, ThemeProvider } from "@mui/material";
import { wloTheme, wloThemeData } from "./wloTheme";

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

  const outletContext: RootContext = {
    sourceItems: sourceItems,
    setStep: setStep,
    onSourceSelected: (source: SourceItem) => {
      setSelectedSourceItem(source);
      setHistoryState({ step: "add-crawler", newCrawlerName: "abcd" });
    },
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
    const response = await fetch("http://localhost:8000/api/crawlers");
    const data: Crawler[] = await response.json();
    // TODO: validate?
    setCrawlerList(data);
  }

  async function fetchSourceItems() {
    const response = await fetch("http://localhost:8000/api/source_items");
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
      <div>
        WLO Header here 
        </div>
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
      <footer>WLO Footer here</footer>
    </div>
    </ThemeProvider>
  );
}