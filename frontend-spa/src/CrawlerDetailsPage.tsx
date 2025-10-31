import { TextField } from "@mui/material";
import { useState } from "react";
import { useOutletContext, useParams } from "react-router-dom";
import sourcePreviewPic from "./assets/source-preview.jpg";
import { CrawlerDetailsPageContext } from "./RootContext";
import { useStep } from "./types";


export default function CrawlerDetailsPage() {
    const { crawlerId } = useParams();
    const { crawlerList, sourceItems } = useOutletContext<CrawlerDetailsPageContext>();
    const crawler = crawlerList.find(c => c.id.toString() === crawlerId);
    const sourceItem = sourceItems.find(s => s.guid === crawler?.sourceItemGuid);

    const [crawlerURL, setCrawlerURL] = useState<string>(crawler?.start_url || "");
    const [crawlerName, setCrawlerName] = useState<string>(crawler?.name || "");

    useStep("crawler-details");

    if (!crawlerId || !crawler) {
        return <div className="main-content">
            <p>Crawler not found</p>
        </div>;
    }

    return <div className="main-content">
        <h1>Crawler Details Page</h1>
        <p>Crawler ID: {crawler.id}</p>

        {sourceItem ? <>
        <div>Quelle:</div>
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
        </>
        : <p>Kein Quellobjekt gefunden</p>}

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
        />
        {/* Add more crawler details here */}
    </div>;

}