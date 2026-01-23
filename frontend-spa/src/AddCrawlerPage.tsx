import TextField from '@mui/material/TextField';
import { useEffect, useState } from "react";
import { useNavigate, useOutletContext, useSearchParams } from "react-router";
// import Button from "./Button";
import { AddCrawlerPageContext } from "./RootContext";
import { createCrawler } from "./apitypes";
import sourcePreviewPic from "./assets/source-preview.jpg";
import { useStep } from "./steps";
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';


export default function AddCrawlerPage() {

  const { sourceItem, setSourceItem, crawlerList, sourceItems, setCrawlerList } = useOutletContext<AddCrawlerPageContext>();

  // const { sourceItem, onCreateClick, onCancelClick } = props;
  const [crawlerURL, setCrawlerURL] = useState<string>("");
  const [crawlerName, setCrawlerName] = useState<string>("");



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
      const existingCrawler = crawlerList.find(c => c.id === existingCrawlerId);
      if (existingCrawler) {
        // override defaultURL with existing crawler's start_url
        setCrawlerURL(existingCrawler.start_url);
        setCrawlerName(existingCrawler.name);
        const sourceItemForCrawler = sourceItems.find(s => s.guid === existingCrawler.source_item);
        if (sourceItemForCrawler) {
          setSourceItem(sourceItemForCrawler);
        }
      }
    }
  }, [crawlerList, existingCrawlerId, setSourceItem, sourceItems]);

  useEffect(() => {
    setCrawlerURL(defaultURL);
  }, [defaultURL]);

  useEffect(() => {
    setCrawlerName(defaultName);
  }, [defaultName]);


  async function onCreateClick() {
    if (!sourceItem) return;
    // create a crawler, and launch an initial analysis-crawl
    const newCrawler = await createCrawler(sourceItem.guid, crawlerURL, crawlerName);
    setCrawlerList([...crawlerList, newCrawler]);
    navigate(`/crawlers/${newCrawler.id}/metadata-inheritance`);
  }

  if (!sourceItem) {
    return <div>Kein Quellobjekt ausgewählt</div>;
  }

  return (
    <div style={{overflowY: "scroll", padding: "0px 24px 24px 24px"}}>
      <div>
        <h2 style={{marginTop: 8}}>Neuen Crawler erstellen</h2>
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
          value={crawlerName}
          onChange={(event) => setCrawlerName(event.target.value)}
          fullWidth
          label="Name des Crawlers"
          style={{ marginBottom: "20px" }}
        />

        <TextField
          value={crawlerURL}
          onChange={(event) => setCrawlerURL(event.target.value)}
          fullWidth
          label="Start-URL"
          disabled={!!existingCrawlerId}
        />

        <Stack direction="row" gap={1} sx={{ mt: 2}}>
          <Button variant="outlined" onClick={() => navigate(-1)}>Zurück</Button>
          {existingCrawlerId
            ? <Button variant="contained" style={{ marginLeft: 'auto' }} onClick={() => navigate(`/crawlers/${existingCrawlerId}/metadata-inheritance`)}>Weiter zur Metadatenvererbung</Button>
            : <Button variant="contained" style={{ marginLeft: 'auto' }} onClick={onCreateClick}>Crawler anlegen</Button>
          }
        </Stack>

      </div>
    </div>
  );
}
