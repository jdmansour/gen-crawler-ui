import { Button as MuiButton } from "@mui/material";
import Stack from "@mui/material/Stack";
import { useState } from "react";
import { useNavigate, useOutletContext } from "react-router-dom";
import Button from "./Button";
import ListView from "./ListView";
import { SelectSourcePageContext } from "./RootContext";
import { SourceItem } from "./apitypes";
import sourcePreviewPic from "./assets/source-preview.jpg";
import { useStep } from "./steps";
export default function SelectSourcePage() {

  const { sourceItems, onSourceSelected } = useOutletContext<SelectSourcePageContext>();

  const [selectedSourceId, setSelectedSourceId] = useState<number | null>(null);
  const navigate = useNavigate();

  useStep("select-source");
  
  return (<div style={{ display: "flex", flexDirection: "column", flex: 1,
                        padding: "16px", gap: "16px" }}>
        <div>Für welches Quellobjekt soll ein Crawler erstellt werden?</div>

        <div style={{ overflowY: "scroll", flexBasis: 100, flexGrow: 1}}>
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
        </div>

        <Stack direction="row" gap={1}>
          <MuiButton variant="outlined" onClick={() => navigate(-1)}>Abbrechen</MuiButton>
          <MuiButton variant="contained" style={{ marginLeft: 'auto' }} 
            disabled={selectedSourceId === null}
            onClick={() => {
              const selectedSource = sourceItems.find(item => item.id === selectedSourceId);
              if (selectedSource && onSourceSelected) {
                onSourceSelected(selectedSource);
              }
          }}>
            Weiter
          </MuiButton>
        </Stack>
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
          onChange={props.onSelect} />
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
