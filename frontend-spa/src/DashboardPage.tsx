import Delete from '@mui/icons-material/Delete';
import ErrorOutlineOutlined from '@mui/icons-material/ErrorOutlineOutlined';
import MoreVertOutlined from '@mui/icons-material/MoreVertOutlined';
import IconButton from '@mui/material/IconButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { useState } from "react";
import { Link, useNavigate, useOutletContext } from "react-router-dom";
import "./App.css";
import DeleteCrawlerDialog from './DeleteCrawlerDialog';
import FilterTabs, { TabInfo } from "./FilterTabs";
import ListView from "./ListView";
import { CrawlerDetailsContext, CrawlerDetailsPageContext, DashboardPageContext } from "./RootContext";
import { Crawler, CrawlerStatus } from "./apitypes";
import { useStep } from "./steps";
import { CrawlerDetails } from './CrawlerDetailsPage';
import { createPortal } from 'react-dom';

const crawlerStateLabels: { [key in CrawlerStatus]: string } = {
  draft: "Entwurf",
  pending: "Gecrawlt",
  stopped: "Gestoppt",
  error: "Fehler",
  published: "Im Prüfbuffet",
};

export default function DashboardPage() {
  const { crawlerList = [], setSidebarVisible } = useOutletContext<DashboardPageContext>();
  const [activeTab, setActiveTab] = useState(0);
  const navigate = useNavigate();

  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [menuCrawlerId, setMenuCrawlerId] = useState<number | null>(null);
  const menuOpen = Boolean(anchorEl);

  const [crawlerDeleteDialogOpen, setCrawlerDeleteDialogOpen] = useState(false);
  const [selectedCrawlerId, setSelectedCrawlerId] = useState<number | null>(null);

  // for the sidebar
  const { sourceItems, onCrawlJobDeleted, onCrawlJobLiveUpdate } = useOutletContext<CrawlerDetailsPageContext>();
  const { deleteCrawler } = useOutletContext<CrawlerDetailsContext>();

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>, crawlerId: number) => {
    setAnchorEl(event.currentTarget);
    setMenuCrawlerId(crawlerId);
    event.stopPropagation();
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

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

  const sidebarOutlet = document.getElementById("sidebar-outlet");

  return (
    <>
      <FilterTabs
        tabs={tabs}
        selectedTab={activeTab}
        onTabClick={(index) => setActiveTab(index)}
      />
      <div style={{ overflowY: "overlay", flex: 1, marginTop: "-20px", paddingTop: "20px", marginBottom: "-20px", paddingBottom: "20px", paddingLeft: "40px", paddingRight: "40px"}}>
        <ListView style={{ width: "100%", boxSizing: "border-box" }}>
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
            <CrawlerTableRow key={info.id} info={info} menuOpen={menuOpen} handleMenuClick={handleMenuClick}
              onClick={() => {
                setSelectedCrawlerId(info.id);
                setSidebarVisible(true);
              }}/>
          ))}
        </ListView>

        <Menu id="crawler-menu"
            anchorEl={anchorEl}
            open={menuOpen}
            onClose={handleMenuClose}
            slotProps={{
                list: {'aria-labelledby': 'crawler-button'},
            }}
            anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
            transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        >
          <MenuItem onClick={handleMenuClose}
          >Hallo</MenuItem>
            <MenuItem onClick={() => {
              handleMenuClose();
              navigate(`crawlers/${menuCrawlerId}`);
            }}>
              <ListItemIcon><MoreVertOutlined fontSize="small" /></ListItemIcon>
              Details anzeigen
            </MenuItem>

          <MenuItem sx={{ color: 'error.main' }}
              onClick={() => {
                handleMenuClose();
                setCrawlerDeleteDialogOpen(true);
              }}>
              <ListItemIcon sx={{ color: 'error.main' }}><Delete fontSize="small" /></ListItemIcon>
                Crawler {menuCrawlerId} löschen
            </MenuItem>
        </Menu>
        <DeleteCrawlerDialog
          open={crawlerDeleteDialogOpen}
          onClose={() => setCrawlerDeleteDialogOpen(false)}
          onConfirm={() => {setCrawlerDeleteDialogOpen(false); if (menuCrawlerId) deleteCrawler(menuCrawlerId);}} />
      </div>
      <hr />
      {/* <div style={{ backgroundColor: "#f9f9f9", padding: "10px", fontSize: "0.9em", color: "#666666", margin: 20 }}>
        {filteredCrawlerList.length} Crawler angezeigt, insgesamt {crawlerList.length} Crawler.
      </div> */}

      {sidebarOutlet && (createPortal((
        (selectedCrawlerId === null) ?
        <div style={{ padding: "20px" }}>Kein Crawler ausgewählt</div> :
        <CrawlerDetails
          crawlerId={selectedCrawlerId}
          crawlerList={crawlerList}
          sourceItems={sourceItems}
          onCrawlJobDeleted={onCrawlJobDeleted}
          onCrawlJobLiveUpdate={onCrawlJobLiveUpdate}
        />), sidebarOutlet))}
    </>
  );
}

function CrawlerTableRow(props: {
  info: Crawler,
  onClick?: (crawlerId: number) => void,
  menuOpen: boolean,
  handleMenuClick: (event: React.MouseEvent<HTMLElement>, crawlerId: number) => void,
}) {
  const updatedAt = new Date(props.info.updated_at);
  return (
    <tr onClick={() => props.onClick && props.onClick(props.info.id)} style={{ cursor: props.onClick ? "pointer" : "default" }}>
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
        <IconButton
          aria-controls={props.menuOpen ? 'crawler-job-menu' : undefined}
          aria-haspopup="true"
          aria-expanded={props.menuOpen ? 'true' : undefined}
          onClick={(e) => props.handleMenuClick(e, props.info.id)}
        >
          <MoreVertOutlined fontSize="medium" />
        </IconButton>
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
