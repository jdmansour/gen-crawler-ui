
import { FormGroup, Button as MUIButton, Skeleton } from "@mui/material";
import Grid from "@mui/system/Grid";
import { useEffect, useState } from "react";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import Button from "./Button";
import MdsEditor from "./MdsEditor";
import { MetadataInheritancePageContext } from "./RootContext";
import WloFieldGroupSet from "./WloFieldGroupSet";
import { useStep } from "./types";
import { fieldMissing, GroupInfo, WloFieldInfo } from "./wloTypes";

export default function MetadataInheritancePage() {
  const { onSave, crawlerList } = useOutletContext<MetadataInheritancePageContext>();
  const navigate = useNavigate();
  const params = useParams();
  const crawlerId: number | undefined = params.crawlerId ? parseInt(params.crawlerId) : undefined;
  const crawler = crawlerList.find(c => c.id === crawlerId);
  const sourceItemGuid = crawler?.sourceItemGuid;

  const [selectedFields, setSelectedFields] = useState<Record<string, boolean>>({});
  const [fields, setFields] = useState<WloFieldInfo[]>([]);
  const [groups, setGroups] = useState<GroupInfo[]>([]);
  const [sourceFieldsLoading, setSourceFieldsLoading] = useState(false);

  useStep("metadata-inheritance");

  async function fetchSourceFields(sourceItemGuid: string) {
    setSourceFieldsLoading(true);
    const response = await fetch(`http://localhost:8000/api/source_items/${sourceItemGuid}/inheritable_fields`);
    const data = await response.json();

    // sleep 2 seconds to simulate loading
    await new Promise((resolve) => setTimeout(resolve, 2000));

    console.log("Fetched source fields:", data);
    setFields(data.fields as WloFieldInfo[]);
    setGroups(data.groups as GroupInfo[]);
    setSourceFieldsLoading(false);

    return data;
  }

  useEffect(() => {
    if (sourceItemGuid) {
      fetchSourceFields(sourceItemGuid);
    }
  }, [sourceItemGuid]);

  function selectAllRecommendedFields() {
    const tmp = { ...selectedFields };
    for (const field of fields) {
      console.log("Checking field:", field.id);
      const missing = fieldMissing(field);

      if (field.recommended && !missing) {
        if (!tmp[field.id]) {
          tmp[field.id] = true;
        }
      }
    }
    setSelectedFields(tmp);
  }

  return <div className="main-content">
    <div>
      <h2>Metadatenvererbung</h2>
      <p>Dein neuer Crawler wurde erstellt! Während im Hintergrund die Quelle analysiert wird, kannst du jetzt schon mal die Felder auswählen, die von dem Quelldatensatz übernommen werden sollen.</p>
      <FormGroup style={{ marginBottom: "1em" }}>
        {/* <MUIButton onClick={() => setSourceFieldsLoading(x => !x)}>Toggle Loading</MUIButton> */}
        <MUIButton onClick={selectAllRecommendedFields}>Alle empfohlenen Felder auswählen</MUIButton>
      </FormGroup>

      {sourceFieldsLoading ?
        <Grid container spacing={2}>
          <Grid size={{ xs: 12, md: 12 }}>
            <MdsEditor title={<Skeleton animation="wave" variant="text" width={100} />}
              icon={<Skeleton animation="wave" variant="circular" width={28} height={28} style={{ flexShrink: 0 }} />}>
              <Skeleton animation="wave" variant="text" height={40} />
              <Skeleton animation="wave" variant="text" height={40} />
              <Skeleton animation="wave" variant="text" height={40} />
            </MdsEditor>

          </Grid>
          <Grid size={{ xs: 12, md: 6 }}>
            <MdsEditor title={<Skeleton animation="wave" variant="text" width={100} />}
              icon={<Skeleton animation="wave" variant="circular" width={28} height={28} style={{ flexShrink: 0 }} />}>
              <Skeleton animation="wave" variant="text" height={40} />
              <Skeleton animation="wave" variant="text" height={40} />
              <Skeleton animation="wave" variant="text" height={40} />
            </MdsEditor>
          </Grid>
          <Grid size={{ xs: 12, md: 6 }}>
            <MdsEditor title={<Skeleton animation="wave" variant="text" width={100} />}
              icon={<Skeleton animation="wave" variant="circular" width={28} height={28} style={{ flexShrink: 0 }} />}>
              <Skeleton animation="wave" variant="text" height={40} />
              <Skeleton animation="wave" variant="text" height={40} />
              <Skeleton animation="wave" variant="text" height={40} />
            </MdsEditor>
          </Grid>
        </Grid>
        :
        <WloFieldGroupSet groups={groups} fields={fields} selectedFields={selectedFields} onSelectedFieldsChange={
          (update) => {
            console.log("Field selection update:", update);
            setSelectedFields(prev => {
              return { ...prev, ...update };
            });
          }}
        />
      }

      <div className="wlo-button-group">
        <Button leftAlign onClick={() => navigate(-1)}>
          Zurück
        </Button>
        <Button
          default
          onClick={() => {
            // console.log("Selected fields:", selectedFields);
            onSave?.(selectedFields);
          }
            // setHistoryState({
            //     step: "filter-crawls",
            //     newCrawlerName: newCrawlerName,
            // })
          }
        >
          Weiter
        </Button>
      </div>
    </div>
  </div>
}