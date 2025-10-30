// RootLayout.tsx
import { useEffect, useState } from "react";
import { Outlet, useNavigate, useParams } from "react-router-dom";
import { CrawlerResponse, createCrawler, SourceItem } from "./apitypes";
import Breadcrumbs, { Breadcrumb } from "./Breadcrumbs";
import GenCrawlerSidebar from "./GenCrawlerSidebar";
import { RootContext } from "./RootContext";
import SiteLayout, { ShowSidebarButton } from "./SiteLayout";
import { CrawlerDashboardStep, CrawlerInfo } from "./types";
import { GroupInfo, WloFieldInfo } from "./wloTypes";

export default function RootLayout() {
  const [sidebarVisible, setSidebarVisible] = useState(true);

  const [crawlerList, setCrawlerList] = useState<CrawlerInfo[]>([]);
  // select source
  const [sourceItems, setSourceItems] = useState<SourceItem[]>([]);
  const [selectedSourceItem, setSelectedSourceItem] = useState<SourceItem | null>(null);

  // metadata inheritance
  const [fields, setFields] = useState<WloFieldInfo[]>([]);
  const [fieldGroups, setFieldGroups] = useState<GroupInfo[]>([]);
  // used while loading source fields
  const [sourceFieldsLoading, setSourceFieldsLoading] = useState(false);

  const [step, setStep] = useState<CrawlerDashboardStep>("dashboard");
  const params = useParams();
  const crawlerId = params.crawlerId;
  console.log("RootLayout params:", params)


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
    sourceItem: selectedSourceItem || undefined,
    onCreateClick: async (sourceItem: SourceItem, crawlerURL: string, crawlerName: string) => {
      fetchSourceFields(sourceItem.guid);
      // todo: add crawler
      console.log("Creating crawler for source:", sourceItem, "with URL:", crawlerURL);

      // create a crawler, and launch an initial analysis-crawl
      const newCrawler = await createCrawler(sourceItem.guid, crawlerURL, crawlerName);

      console.log("Created new crawler:", newCrawler);

      //setHistoryState({ step: `crawlers/${newCrawler.id}/metadata-inheritance`, newCrawlerName: crawlerName });
      navigate(`/crawlers/${newCrawler.id}/metadata-inheritance`);
    },
    fields: fields,
    groups: fieldGroups,
    onSave: async (selectedFields: Record<string, boolean>) => {
      console.log("Selected fields to inherit:", selectedFields);
      if (crawlerId === null) {
          console.error("No crawler ID found!");
          return;
      }
      const inheritedFields = Object.keys(selectedFields).filter(fieldId => selectedFields[fieldId]);
      console.log("Updating crawler", crawlerId, "with inherited fields:", inheritedFields);
      const response = await fetch(`http://localhost:8000/api/crawlers/${crawlerId}/`, {
          method: "PATCH",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({
              inherited_fields: inheritedFields
          })
      });
      if (!response.ok) {
          console.error("Failed to update crawler:", response.status, response.statusText);
          return;
      }
      console.log("Crawler updated successfully.");
      //setHistoryState({ step: "filter-crawls", newCrawlerName: crawlerName || undefined });

    }
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
    // is the id in the list?
    const crawlerFound = crawlerId && crawlerList.find(c => c.id == crawlerId);
    console.log("Displaying breadcrumbs for crawlerId:", crawlerId, "found:", crawlerFound);
    const crawlerName = crawlerList.find(c => c.id == crawlerId)?.name;
    breadcrumbs.push({ label: crawlerName || "-", url: `/crawlers/${crawlerId}` });
  }

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

  return (
    <div>
      <header>Header stuff here</header>
      <SiteLayout
        sidebar={<GenCrawlerSidebar step={step} />}
        sidebarVisible={sidebarVisible}
        onSidebarClose={() => setSidebarVisible(false)} >
        {!sidebarVisible && (
          <ShowSidebarButton onClick={() => setSidebarVisible(true)} />
        )}

        <Breadcrumbs breadcrumbs={breadcrumbs} />
        <Outlet context={outletContext} />
      </SiteLayout>
      <footer>Footer stuff here</footer>
    </div>
  );
}