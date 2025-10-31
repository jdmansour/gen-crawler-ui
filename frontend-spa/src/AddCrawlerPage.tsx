import { TextField } from "@mui/material";
import { useEffect, useState } from "react";
import { useNavigate, useOutletContext, useParams, useSearchParams } from "react-router";
import Button from "./Button";
import { AddCrawlerPageContext } from "./RootContext";
import { SourceItem } from "./apitypes";
import sourcePreviewPic from "./assets/source-preview.jpg";
import { useStep } from "./types";


export default function AddCrawlerPage() {

  const { sourceItem, onCreateClick } = useOutletContext<AddCrawlerPageContext>();

  // const { sourceItem, onCreateClick, onCancelClick } = props;
  const [ crawlerURL, setCrawlerURL ] = useState<string>("");
  const [ crawlerName, setCrawlerName ] = useState<string>("");

  useStep("add-crawler");

  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  // if we go back to add-crawler from a later step, we might have an existing crawlerId
  const crawlerIdString = searchParams.get("crawlerId");
  const existingCrawlerId = crawlerIdString ? parseInt(crawlerIdString) : undefined;

  // default start URL
  const defaultURL = sourceItem?.data?.properties['ccm:wwwurl'][0] || "";
  const defaultName = sourceItem?.title || "";

  useEffect(() => {
    if (existingCrawlerId) {
      // If we have an existing crawlerId, we should load the existing crawler data
      // TODO: Implement loading existing crawler data
      console.log("Would load existing crawler data for ID:", existingCrawlerId);
    }
  }, [existingCrawlerId]);

  useEffect(() => {
    setCrawlerURL(defaultURL);
  }, [defaultURL]);

  useEffect(() => {
    setCrawlerName(defaultName);
  }, [defaultName]);


  if (!sourceItem) {
    return <div>Kein Quellobjekt ausgewählt</div>;
  }


  return (
    <div className="main-content">
      <div>
        <h2>Neuen Crawler erstellen</h2>
        {existingCrawlerId && (
          <p>Dieser crawler wurde bereits angelegt, du kannst hier den Namen noch ändern.</p>
        )}

        <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "20px" }}>
          <img
            src={sourceItem.preview_url || sourcePreviewPic}
            alt="Vorschau"
            className="source-preview"
            style={{
              maxWidth: 80,
              maxHeight: 60,
            }} />
          {sourceItem.title}
        </div>

        <TextField
          value={crawlerURL}
          onChange={(event) => setCrawlerURL(event.target.value)}
          fullWidth
          label="Start-URL"
          disabled={!!existingCrawlerId}
        />

        <TextField
          value={crawlerName}
          onChange={(event) => setCrawlerName(event.target.value)}
          fullWidth
          label="Name des Crawlers"
          style={{ marginTop: "20px" }}
        />

        <div className="wlo-button-group">
          <Button leftAlign onClick={() => navigate(-1)}>Zurück</Button>
          <Button default onClick={() => {
            if (onCreateClick) {
              onCreateClick(sourceItem, crawlerURL, crawlerName);
            }
          }}>
            Crawler anlegen
          </Button>
        </div>
      </div>
    </div>
  );
}

export function InheritanceTableRow(props: {
  item: SourceItem;
  selected: boolean;
  onSelect: () => void;
}) {
  return (
    <tr
      className={"with-checkbox" + (props.selected ? " selected" : "")}
      onClick={(event) => {
        if (shouldCancelClick(event)) {
          return;
        }
        props.onSelect();
      }}
    >
      <td className="checkbox-column">
        <input
          type="radio"
          id={"checkbox-" + props.item.id}
          checked={props.selected}
          onClick={props.onSelect} />
      </td>
      <td className="main-column">
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <img
            src={props.item.preview_url || sourcePreviewPic}
            alt="Vorschau"
            className="source-preview"
            style={{
              maxWidth: 80,
              maxHeight: 60,
            }} />
          {props.item.title}
        </div>
      </td>
      <td>
        <div className="inline-title">Fachgebiet</div>Deutsch
      </td>
      <td>
        <div className="inline-title">Redaktion</div>WLO-OER
      </td>
    </tr>
  );
}

function shouldCancelClick(event: React.MouseEvent) {
  const target = event.target as HTMLElement;
  const selection = window.getSelection();
  const text_selected = selection && selection.toString();
  if (target.tagName === "INPUT") {
    return true;
  }
  if (target.tagName === "A" || text_selected) {
    return true;
  }
  return false;
}
