import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Button from "./Button";
import ListView from "./ListView";
import { SourceItem } from "./apitypes";
import sourcePreviewPic from "./assets/source-preview.jpg";
import { CrawlerDashboardStep } from "./types";

export default function SelectSourcePage(props: {
  sourceItems: SourceItem[];
  onSourceSelected?: (source: SourceItem) => void;
}) {
  
  const { sourceItems } = props;

  const [selectedSourceId, setSelectedSourceId] = useState<number | null>(null);

  const navigate = useNavigate();
  const location = useLocation();

  const newCrawlerName = location.state?.newCrawlerName || "";

  function setHistoryState(state: {
    step: CrawlerDashboardStep;
    newCrawlerName?: string;
  }) {
    const loc = "#" + state.step;
    navigate(loc, { state: state, replace: false });
  }

  return (
    <div className="main-content">
      <div>
        <h2>Vererbungsquelle wählen xx</h2>
        <p>New dashboard source '{newCrawlerName}'</p>

        <ListView>
          {sourceItems.map((item) => (
            <InheritanceTableRow
              key={item.id}
              item={item}
              selected={selectedSourceId == item.id}
              onSelect={() => setSelectedSourceId(item.id)}
            />
          ))}
        </ListView>

        <div className="wlo-button-group">
          <Button leftAlign onClick={() => navigate(-1)}>
            Abbrechen
          </Button>
          <Button>Quelldaten neu anlegen</Button>
          <Button default onClick={() => {
            if (props.onSourceSelected && selectedSourceId !== null) {
              const selectedSource = sourceItems.find(item => item.id === selectedSourceId);
              if (selectedSource) {
                props.onSourceSelected(selectedSource);
              }
            }
            setHistoryState({ step: "metadata-inheritance", newCrawlerName });
          }}>
            Weiter mit Vererbung
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
