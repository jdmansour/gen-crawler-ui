import { useNavigate, useParams } from "react-router-dom";
import FilterCrawlsIcon from "./assets/icons/filter-crawls.svg?react";
import MetadataInheritanceIcon from "./assets/icons/metadata-inheritance.svg?react";
import RobotIcon from "./assets/icons/robot.svg?react";
import SelectSourceIcon from "./assets/icons/select-source.svg?react";
import FilterTabs, { TabInfo } from "./FilterTabs";
import { CrawlerDashboardStep } from "./steps";

export default function GenCrawlerSidebar(props: {
  step: CrawlerDashboardStep;
}) {
  const sidebarTabs = [
    // { tag: "dashboard", label: "1. Dashboard.", icon: RobotIcon },
    { tag: "select-source", label: "1. Quelle Wählen", icon: SelectSourceIcon },
    { tag: "add-crawler", label: "2. Crawler Details", icon: RobotIcon },
    { tag: "metadata-inheritance", label: "3. Datenvererbung", icon: MetadataInheritanceIcon },
    { tag: "filter-crawls", label: "4. Filtern", icon: FilterCrawlsIcon },
  ] as TabInfo[];

  const { step } = props;
  const activeSidebarTab = sidebarTabs.findIndex((tab) => tab.tag == step);
  const navigate = useNavigate();
  const params = useParams();
  console.log("Rendering sidebar for step:", step);

  return (
    <FilterTabs
      tabs={sidebarTabs}
      style="sidebar"
      selectedTab={activeSidebarTab}
      tabsClickable="complete"
      onTabClick={(index) => {
        const tag = sidebarTabs[index].tag;
        const crawlerId = params.crawlerId;

        switch (tag) {
          case "select-source":
            navigate(`/${tag}`);
            break;
          case "add-crawler":
            {
              let url = `/${tag}`;
              if (crawlerId) {
                url += `?crawlerId=${crawlerId}`;
              }
              navigate(url);
              break;
            }
          case "metadata-inheritance":
          case "filter-crawls":
            navigate(`/crawlers/${crawlerId}/${tag}`);
            break;
          default:
            console.error("Unhandled sidebar tab click for tag:", tag);
            return;
        }
      }}
    />
  );
}
