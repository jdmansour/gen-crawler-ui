import { Paper, Tab, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField } from "@mui/material";
import { useState } from "react";
import { useOutletContext, useParams } from "react-router-dom";
import sourcePreviewPic from "./assets/source-preview.jpg";
import { CrawlerDetailsPageContext } from "./RootContext";
import { useStep } from "./steps";


export default function CrawlerDetailsPage() {
    const { crawlerId } = useParams();
    const { crawlerList, sourceItems } = useOutletContext<CrawlerDetailsPageContext>();
    const crawler = crawlerList.find(c => c.id.toString() === crawlerId);
    const sourceItem = sourceItems.find(s => s.guid === crawler?.source_item);

    const [crawlerURL, setCrawlerURL] = useState<string>(crawler?.start_url || "");
    const [crawlerName, setCrawlerName] = useState<string>(crawler?.name || "");

    useStep("crawler-details");

    if (!crawlerId || !crawler) {
        return <div className="main-content">
            <p>Crawler not found</p>
        </div>;
    }

    return <div className="main-content">
        <h1>Crawler-Details</h1>
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

        <p><a href={`http://localhost:8000/admin/crawls/crawler/${crawler.id}/change/`}>Im Admin-Bereich anzeigen</a></p>

        <h2>Läufe des Crawlers</h2>

        <TableContainer component={Paper}>
        <Table>
            <TableHead>
                <TableRow>
                    <TableCell>Start URL</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Erstellt am</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {crawler.crawl_jobs.map(job => (
                    <TableRow key={job.id}>
                        <TableCell>{job.start_url}</TableCell>
                        <TableCell>{job.state}</TableCell>
                        <TableCell>{new Date(job.created_at).toLocaleString("de-DE")}</TableCell>
                    </TableRow>
                ))}
                {(crawler.crawl_jobs.length === 0) && (
                    <TableRow>
                        <TableCell colSpan={3}>No crawl jobs found.</TableCell>
                    </TableRow>
                )}
            </TableBody>
        </Table>
        </TableContainer>

    </div>;

}