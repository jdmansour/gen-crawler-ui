import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./App.css";
import Breadcrumbs, { Breadcrumb } from "./Breadcrumbs";
import "./Button.css";
import DashboardPage from "./DashboardPage";
import FilterCrawlsPage from "./FilterCrawlsPage";
import GenCrawlerSidebar from "./GenCrawlerSidebar";
import MetadataInheritancePage from "./MetadataInheritancePage";
import SelectSourcePage from "./SelectSourcePage";
import SiteLayout, { ShowSidebarButton } from "./SiteLayout";

import { CrawlerResponse, createCrawler, SourceItem } from "./apitypes";
import { CrawlerDashboardStep, CrawlerInfo } from "./types";
import { GroupInfo, WloFieldInfo } from "./wloTypes";
import CrawlerDetailsPage from "./CrawlerDetailsPage";

export default function App() {
  const location = useLocation();
  const [sidebarVisible, setSidebarVisible] = useState(false);
  const [crawlerList, setCrawlerList] = useState<CrawlerInfo[]>([]);
  const [sourceItems, setSourceItems] = useState<SourceItem[]>([]);
  const [selectedSourceItem, setSelectedSourceItem] = useState<SourceItem | null>(null);
  const [fields, setFields] = useState<WloFieldInfo[]>([]);
  const [fieldGroups, setFieldGroups] = useState<GroupInfo[]>([]);
  const [sourceFieldsLoading, setSourceFieldsLoading] = useState(false);
  const step = location.state?.step || "dashboard";

  const breadcrumbs: Breadcrumb[] = [
    { label: "Startseite", url: "/" },
    { label: "Quellen", url: "/" },
    { label: "Generischer Crawler", url: "/" },
  ];
  if (step != "dashboard") {
    // Add breadcrumb for current crawler
    breadcrumbs.push({ label: "Neuer Crawler", temporary: true });
  }

  useEffect(() => {
    // Set the document title
    document.title = `Generic crawler (${step})`;
  }, [step]);

  async function fetchCrawlers() {
    const response = await fetch("http://localhost:8000/api/crawlers");
    const data: CrawlerResponse[] = await response.json();

    console.log("Fetched crawlers:", data);

    // Map the API response to the CrawlerInfo type
    const crawlers = data.map(item => new CrawlerInfo(
      item.id,
      item.name,
      "pending",
      new Date(item.updated_at)
    ));
    setCrawlerList(crawlers);
  }

  async function fetchSourceItems() {
    const response = await fetch("http://localhost:8000/api/source_items");
    const data: SourceItem[] = await response.json();

    console.log("Fetched source items:", data);

    setSourceItems(data);
  }

  async function fetchSourceFields(sourceItemGuid: string) {
    setSourceFieldsLoading(true);
    const response = await fetch(`http://localhost:8000/api/source_items/${sourceItemGuid}/inheritable_fields`);
    const data = await response.json();

    console.log("Fetched source fields:", data);
    setFields(data.fields as WloFieldInfo[]);
    setFieldGroups(data.groups as GroupInfo[]);
    setSourceFieldsLoading(false);

    return data;
  }

  useEffect(() => {
    fetchCrawlers();
    fetchSourceItems();
  }, []);

  const navigate = useNavigate();
    function setHistoryState(state: {
    step: CrawlerDashboardStep;
    newCrawlerName?: string;
  }) {
    const loc = "#" + state.step;
    navigate(loc, { state: state, replace: false });
  }

  return (
    <>
    <p>This is the main app</p>
      <SiteLayout
        sidebar={<GenCrawlerSidebar step={step} />}
        sidebarVisible={sidebarVisible}
        onSidebarClose={() => setSidebarVisible(false)}
      >
        {!sidebarVisible && (
          <ShowSidebarButton onClick={() => setSidebarVisible(true)} />
        )}
        <Breadcrumbs breadcrumbs={breadcrumbs} />
        {step == "dashboard" && (
          <>
          <DashboardPage crawlerList={crawlerList}
            onNewCrawlerClick={()=>{
              setHistoryState({ step: "select-source" });
            }}/>
            </>
        )}
        {step == "select-source" && (
          <SelectSourcePage
            sourceItems={sourceItems}
            onSourceSelected={(sourceItem) => {
              setSelectedSourceItem(sourceItem);
              setHistoryState({ step: "crawler-details", newCrawlerName: "abcd" });
            }}
            onCancelClick={() => navigate(-1)}
            />
        )}
        {step == "crawler-details" && (
          selectedSourceItem && (
          <CrawlerDetailsPage
            sourceItem={selectedSourceItem}
            onCreateClick={async (sourceItem, crawlerURL, crawlerName) => {
              fetchSourceFields(sourceItem.guid);
              console.log("Creating crawler for source:", sourceItem, "with URL:", crawlerURL);

              // create a crawler, and launch an initial analysis-crawl
              const newCrawler = await createCrawler(sourceItem.guid, crawlerURL, crawlerName);

              console.log("Created new crawler:", newCrawler);

              setHistoryState({ step: "metadata-inheritance", newCrawlerName: "abcd" });
            }}
          />)
        )}
        {step == "metadata-inheritance" && (
          (sourceFieldsLoading === true) ? (
            <p>Lade Quelle</p>
          ) : (
          <MetadataInheritancePage fields={fields} groups={fieldGroups} />
          )
        )}
        {step == "filter-crawls" && (
          <FilterCrawlsPage />
        )}
      </SiteLayout>
    </>
  );
}

