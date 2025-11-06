import Button from '@mui/material/Button';
import Skeleton from '@mui/material/Skeleton';
import Stack from '@mui/material/Stack';
import Grid from "@mui/system/Grid";
import { useEffect, useState } from "react";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import MdsEditor from "./MdsEditor";
import { MetadataInheritancePageContext } from "./RootContext";
import WloFieldGroupSet from "./WloFieldGroupSet";
import { getInheritableFields } from "./apitypes";
import { useStep } from "./steps";
import { fieldMissing, GroupInfo, WloFieldInfo } from "./wloTypes";

export default function MetadataInheritancePage() {
  const { crawlerList } = useOutletContext<MetadataInheritancePageContext>();
  const navigate = useNavigate();
  const params = useParams();
  const crawlerId: number | undefined = params.crawlerId ? parseInt(params.crawlerId) : undefined;
  const crawler = crawlerList.find(c => c.id === crawlerId);
  const sourceItemGuid = crawler?.source_item;

  const [selectedFields, setSelectedFields] = useState<Record<string, boolean>>({});
  const [fields, setFields] = useState<WloFieldInfo[]>([]);
  const [groups, setGroups] = useState<GroupInfo[]>([]);
  const [sourceFieldsLoading, setSourceFieldsLoading] = useState(false);

  useStep("metadata-inheritance");

  async function onSave() {
      if (crawlerId === null) {
          console.error("No crawler ID found!");
          return;
      }
      const inheritedFields = Object.keys(selectedFields).filter(fieldId => selectedFields[fieldId]);
      const response = await fetch(`http://localhost:8000/api/crawlers/${crawlerId}/`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ inherited_fields: inheritedFields })
      });
      if (!response.ok) {
          console.error("Failed to update crawler:", response.status, response.statusText);
          return;
      }
      //setHistoryState({ step: "filter-crawls", newCrawlerName: crawlerName || undefined });
    }

  async function fetchSourceFields(sourceItemGuid: string) {
    setSourceFieldsLoading(true);

    const data = await getInheritableFields(sourceItemGuid);
    
    // sleep 2 seconds to simulate loading
    await new Promise((resolve) => setTimeout(resolve, 2000));

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
      const missing = fieldMissing(field);

      if (field.recommended && !missing) {
        if (!tmp[field.id]) {
          tmp[field.id] = true;
        }
      }
    }
    setSelectedFields(tmp);
  }

  return <div style={{overflowY: "scroll"}}>
      <h2>Metadatenvererbung</h2>
      <p>Dein neuer Crawler wurde erstellt! Während im Hintergrund die Quelle analysiert wird, kannst du jetzt schon mal die Felder auswählen, die von dem Quelldatensatz übernommen werden sollen.</p>
      <Stack direction="row" justifyContent="center" gap={1} sx={{ mb: 2}}>
        <Button variant="outlined" onClick={selectAllRecommendedFields}>Alle empfohlenen Felder auswählen</Button>
      </Stack>

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
            setSelectedFields(prev => {
              return { ...prev, ...update };
            });
          }}
        />
      }

      <Stack direction="row" gap={1} sx={{ mt: 2}}>
        <Button variant="outlined" onClick={() => navigate(-1)}>Zurück</Button>
        <Button variant="contained" style={{ marginLeft: 'auto' }} onClick={onSave}>Weiter</Button>
      </Stack>

      {/* <div className="wlo-button-group">
        <Button leftAlign onClick={() => navigate(-1)}>Zurück</Button>
        <Button default onClick={onSave}>Weiter</Button>
      </div> */}
  </div>
}