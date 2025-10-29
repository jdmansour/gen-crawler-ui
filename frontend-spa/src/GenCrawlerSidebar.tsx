import FilterCrawlsIcon from "./assets/icons/filter-crawls.svg?react";
import MetadataInheritanceIcon from "./assets/icons/metadata-inheritance.svg?react";
import RobotIcon from "./assets/icons/robot.svg?react";
import SelectSourceIcon from "./assets/icons/select-source.svg?react";
import { CrawlerDashboardStep } from "./types";
import FilterTabs, { TabInfo } from "./FilterTabs";
import { useLocation, useNavigate } from "react-router-dom";

export default function GenCrawlerSidebar(props: {
  step: CrawlerDashboardStep;
}) {
  const sidebarTabs = [
    { tag: "dashboard", label: "1. Crawler hinzuf.", icon: RobotIcon },
    { tag: "select-source", label: "2. Quelle Wählen", icon: SelectSourceIcon },
    {
      tag: "metadata-inheritance",
      label: "3. Datenvererbung",
      icon: MetadataInheritanceIcon,
    },
    { tag: "filter-crawls", label: "4. Filtern", icon: FilterCrawlsIcon },
  ] as TabInfo[];

  const { step } = props;
  const activeSidebarTab = sidebarTabs.findIndex((tab) => tab.tag == step);
  const location = useLocation();
  const navigate = useNavigate();
  const historyState = location.state;

  return (
    <FilterTabs
      tabs={sidebarTabs}
      style="sidebar"
      selectedTab={activeSidebarTab}
      tabsClickable="complete"
      onTabClick={(index) => {
        const newState = { ...historyState, step: sidebarTabs[index].tag };
        navigate("/", { state: newState });
      }}
    />
  );
}
