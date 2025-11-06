import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import AddCrawlerPage from "./AddCrawlerPage";
import { Crawler, createCrawler, SourceItem } from "./apitypes";
import "./App.css";
import Breadcrumbs, { Breadcrumb } from "./Breadcrumbs";
import "./Button.css";
import CrawlerDetailsPage from "./CrawlerDetailsPage";
import DashboardPage from "./DashboardPage";
import FilterCrawlsPage from "./FilterCrawlsPage";
import GenCrawlerSidebar from "./GenCrawlerSidebar";
import MetadataInheritancePage from "./MetadataInheritancePage";
import SelectSourcePage from "./SelectSourcePage";
import SiteLayout, { ShowSidebarButton } from "./SiteLayout";
import { CrawlerDashboardStep } from "./steps";
import { GroupInfo, WloFieldInfo } from "./wloTypes";



export default function App() {
  const location = useLocation();
  // layout relevant
  const [sidebarVisible, setSidebarVisible] = useState(false);
  // dashboard
  const [crawlerList, setCrawlerList] = useState<Crawler[]>([]);
  // select source
  const [sourceItems, setSourceItems] = useState<SourceItem[]>([]);
  const [selectedSourceItem, setSelectedSourceItem] = useState<SourceItem | null>(null);
  // metadata inheritance
  const [fields, setFields] = useState<WloFieldInfo[]>([]);
  const [fieldGroups, setFieldGroups] = useState<GroupInfo[]>([]);
  // used while loading source fields
  const [sourceFieldsLoading, setSourceFieldsLoading] = useState(false);
  // used for breadcrumb only
  const [crawlerName, setCrawlerName] = useState<string|null>(null);
  // used for updating the inherited fields of the created crawler
  const [crawlerId, setCrawlerId] = useState<number|null>(null);

  const step = location.state?.step || "dashboard";

  const breadcrumbs: Breadcrumb[] = [
    { label: "Startseite", url: "/" },
    { label: "Quellen", url: "/" },
    { label: "Generischer Crawler", url: "/" },
  ];
  if (step != "dashboard") {
    // Add breadcrumb for current crawler
    if (crawlerName !== null) {
      breadcrumbs.push({ label: crawlerName, url: "/" });
    } else {
      breadcrumbs.push({ label: "Neuer Crawler", temporary: true });
    }
  }

  useEffect(() => {
    // Set the document title
    document.title = `Generic crawler (${step})`;
  }, [step]);

  async function fetchCrawlers() {
    const response = await fetch("http://localhost:8000/api/crawlers");
    const data: Crawler[] = await response.json();

    console.log("Fetched crawlers:", data);

    // Map the API response to the CrawlerInfo type
  //   const crawlers = data.map(item => new CrawlerInfo(
  //     item.id,
  //     item.name,
  //     "pending",
  //     new Date(item.updated_at),
  //     item.source_item
  //   ));
  //   setCrawlerList(crawlers);
  // }
    setCrawlerList(data);
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
    const loc = "/" + state.step;
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
            onCrawlerClick={ (crawlerId) => {
              console.log("Clicked crawler:", crawlerId);
              setHistoryState({ step: "crawler-details", newCrawlerName: "abcd" });
            }}
            onNewCrawlerClick={()=>{
              setCrawlerName(null);
              setHistoryState({ step: "select-source" });
            }}/>
            </>
        )}
        {step == "select-source" && (
          <SelectSourcePage
            sourceItems={sourceItems}
            onSourceSelected={(sourceItem) => {
              setSelectedSourceItem(sourceItem);
              setHistoryState({ step: "add-crawler", newCrawlerName: "abcd" });
            }}
            onCancelClick={() => navigate(-1)}
            />
        )}
        {step == "add-crawler" && (
          selectedSourceItem && (
          <AddCrawlerPage
            sourceItem={selectedSourceItem}
            onCreateClick={async (sourceItem, crawlerURL, crawlerName) => {
              fetchSourceFields(sourceItem.guid);
              console.log("Creating crawler for source:", sourceItem, "with URL:", crawlerURL);

              // create a crawler, and launch an initial analysis-crawl
              const newCrawler = await createCrawler(sourceItem.guid, crawlerURL, crawlerName);

              console.log("Known crawlers before adding new one:", crawlerList);
              console.log("Created new crawler:", newCrawler);

              setCrawlerList([...crawlerList, newCrawler]);

              setCrawlerName(crawlerName);
              setCrawlerId(newCrawler.id);
              setHistoryState({ step: "metadata-inheritance", newCrawlerName: crawlerName });
            }}
          />)
        )}
        {step == "metadata-inheritance" && (
          (sourceFieldsLoading === true) ? (
            <p>Lade Quelle</p>
          ) : (
          <MetadataInheritancePage
            fields={fields}
            groups={fieldGroups}
            onSave={async (selectedFields: Record<string, boolean>) => {
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

            }}
            />
          )
        )}
        {step == "crawler-details" && (
          <CrawlerDetailsPage />
        )}
        {step == "filter-crawls" && (
          <FilterCrawlsPage />
        )}
      </SiteLayout>
    </>
  );
}

