import { useState } from "react";
import "./App.css";
import FilterTabs, { TabInfo } from "./FilterTabs";
import ListView from "./ListView";
import DreipunktmenuIcon from "./assets/icons/dreipunktmenu.svg?react";
import ErrorIcon from "./assets/icons/error.svg?react";
import EditIcon from "./assets/icons/mode_edit.svg?react";
import PendingIcon from "./assets/icons/pending.svg?react";
import StopIcon from "./assets/icons/stop.svg?react";
import { CrawlerInfo, CrawlerStatus } from "./types";

const crawlerStateLabels: { [key in CrawlerStatus]: string } = {
  draft: "Entwurf",
  pending: "Gecrawlt",
  stopped: "Gestoppt",
  error: "Fehler",
  published: "Im Prüfbuffet",
};

export default function DashboardPage(props: {
  crawlerList?: CrawlerInfo[];
  onNewCrawlerClick?: () => void;
}) {
  const [activeTab, setActiveTab] = useState(0);
  const { crawlerList = [], onNewCrawlerClick } = props;

  const tabs = [
    { tag: "all", label: "Alle" },
    { tag: "draft", label: "Entwurf", icon: EditIcon },
    { tag: "pending", label: "Gecrawlt", icon: PendingIcon },
    { tag: "stopped", label: "Gestoppt", icon: StopIcon },
    { tag: "error", label: "Fehler", icon: ErrorIcon },
    { tag: "published", label: "Im Prüfbuffet", icon: ErrorIcon },
    { tag: "published", label: "Im Prüfbuffet", icon: ErrorIcon },
    { tag: "published", label: "Im Prüfbuffet", icon: ErrorIcon },
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
              <button className="wlo-button" onClick={onNewCrawlerClick}>
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

function CrawlerTableRow(props: { info: CrawlerInfo }) {
  return (
    <tr>
      <td className="main-column">
        <a href="#">{props.info.name}</a>
      </td>
      <td>
        <div className="inline-title">Status</div>
        <CrawlerStateLabel state={props.info.status} />
      </td>
      <td>
        <div className="inline-title">zuletzt aktualisiert</div>
        {props.info.updatedAt.toLocaleDateString("de-DE", {
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
        })}
        , {props.info.updatedAt.toLocaleTimeString("de-DE")}
      </td>
      <td className="menu-column">
        <DreipunktmenuIcon width="24" />
      </td>
    </tr>
  );
}

function CrawlerStateLabel(props: { state: CrawlerStatus }) {
  return (
    <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
      {props.state == "error" && <ErrorIcon height={16} color="#ec4a70" />}
      {crawlerStateLabels[props.state]}
    </span>
  );
}
