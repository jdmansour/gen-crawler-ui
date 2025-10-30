import { TextField } from "@mui/material";
import { use, useEffect, useState } from "react";
import Button from "./Button";
import { SourceItem } from "./apitypes";
import sourcePreviewPic from "./assets/source-preview.jpg";

export default function AddCrawlerPage(props: {
  sourceItem: SourceItem;
  onCancelClick?: () => void;
  onCreateClick?: (source: SourceItem, crawlerURL: string, crawlerName: string) => void;
}) {
  
  const { sourceItem, onCreateClick, onCancelClick } = props;
  const [ crawlerURL, setCrawlerURL ] = useState<string>("");
  const [ crawlerName, setCrawlerName ] = useState<string>("");

  // default start URL
  const defaultURL = sourceItem.data?.properties['ccm:wwwurl'][0] || "";
  const defaultName = sourceItem.title || "";

  useEffect(() => {
    setCrawlerURL(defaultURL);
  }, [defaultURL]);

  useEffect(() => {
    setCrawlerName(defaultName);
  }, [defaultName]);

  return (
    <div className="main-content">
      <div>
        <h2>Neuen Crawler erstellen</h2>
        <p>Ausgewählte Quelle:</p>

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
        />

        <TextField
          value={crawlerName}
          onChange={(event) => setCrawlerName(event.target.value)}
          fullWidth
          label="Name des Crawlers"
          style={{ marginTop: "20px" }}
        />

        <div className="wlo-button-group">
          <Button leftAlign onClick={onCancelClick}>Zurück</Button>
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
