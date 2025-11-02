import { ErrorOutlineOutlined, MoreVertOutlined } from "@mui/icons-material";
import { useState } from "react";
import { Link, useNavigate, useOutletContext } from "react-router-dom";
import "./App.css";
import FilterTabs, { TabInfo } from "./FilterTabs";
import ListView from "./ListView";
import { DashboardPageContext } from "./RootContext";
import { Crawler, CrawlerStatus } from "./apitypes";
import { useStep } from "./steps";

const crawlerStateLabels: { [key in CrawlerStatus]: string } = {
  draft: "Entwurf",
  pending: "Gecrawlt",
  stopped: "Gestoppt",
  error: "Fehler",
  published: "Im Prüfbuffet",
};

export default function DashboardPage() {
  const { crawlerList = [] } = useOutletContext<DashboardPageContext>();
  const [activeTab, setActiveTab] = useState(0);
  const navigate = useNavigate();

  useStep("dashboard");

  const tabs = [
    { tag: "all", label: "Alle" },
    { tag: "draft", label: "Entwurf", icon: "edit" },
    { tag: "pending", label: "Gecrawlt", icon: "pending" },
    { tag: "stopped", label: "Gestoppt", icon: "stop" },
    { tag: "error", label: "Fehler", icon: "error" },
    { tag: "published", label: "Im Prüfbuffet", icon: "error" },
  ] as TabInfo[];

  const filterState = tabs[activeTab].tag;
  const filteredCrawlerList = crawlerList.filter((crawler) => {
    if (filterState == "all") {
      return true;
    }
    return crawler.status == filterState;
  });

  return (
    <>
      <FilterTabs
        tabs={tabs}
        selectedTab={activeTab}
        onTabClick={(index) => setActiveTab(index)}
      />
      <div className="main-content">
        <ListView>
          <tr key="add">
            <td colSpan={4} className="action-cell">
              <button className="wlo-button" onClick={() => {
                navigate("/select-source");
              }}>
                + &nbsp;&nbsp; Crawler hinzufügen
              </button>
            </td>
          </tr>
          {filteredCrawlerList.map((info) => (
            <CrawlerTableRow key={info.id} info={info} />
          ))}
        </ListView>
      </div>
    </>
  );
}

function CrawlerTableRow(props: { info: Crawler, onClick?: (crawlerId: number) => void }) {
  const updatedAt = new Date(props.info.updated_at);
  return (
    <tr>
      <td className="main-column">
        <Link to={"crawlers/" + props.info.id + ""}>{props.info.name}</Link>
      </td>
      <td>
        <div className="inline-title">Status</div>
        <CrawlerStateLabel state={props.info.status || "error"} />
      </td>
      <td>
        <div className="inline-title">zuletzt aktualisiert</div>
        {updatedAt.toLocaleDateString("de-DE", {
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
        })}
        , {updatedAt.toLocaleTimeString("de-DE")}
      </td>
      <td className="menu-column">
        <MoreVertOutlined fontSize="medium" />
      </td>
    </tr>
  );
}

function CrawlerStateLabel(props: { state: CrawlerStatus }) {
  return (
    <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
      {props.state == "error" && <ErrorOutlineOutlined sx={{ color: "#ec4a70", fontSize: "1.2em" }} />}
      {crawlerStateLabels[props.state]}
    </span>
  );
}
