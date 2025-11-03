import { Box, Chip, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField } from "@mui/material";
import { DateTime } from "luxon";
import { useEffect, useState } from "react";
import { useOutletContext, useParams } from "react-router-dom";
import { Crawler, CrawlJob } from "./apitypes";
import sourcePreviewPic from "./assets/source-preview.jpg";
import { SSEData, useCrawlerSSE } from "./hooks/useSSE";
import { CrawlerDetailsPageContext } from "./RootContext";
import { useStep } from "./steps";

function mergeCrawlJob(job: CrawlJob, update: Partial<CrawlJob>): CrawlJob {
    if (job.id !== update.id) return job;
    return { ...job, ...update };
}
function mergeCrawler(c: Crawler, sseData: SSEData): Crawler {
    if (c.id !== sseData.crawler_id) return c;
    return { ...c,
            crawl_jobs: c.crawl_jobs.map(job => mergeCrawlJob(job, sseData.crawl_job)) };
};

export default function CrawlerDetailsPage() {
    const { crawlerId } = useParams();
    const { crawlerList, sourceItems, setCrawlerList } = useOutletContext<CrawlerDetailsPageContext>();
    const crawler = crawlerList.find(c => c.id.toString() === crawlerId);
    const sourceItem = sourceItems.find(s => s.guid === crawler?.source_item);
    const [crawlerURL, setCrawlerURL] = useState<string>("");
    const [crawlerName, setCrawlerName] = useState<string>("");

    // Set initial form values when 'crawler' is loaded
    useEffect(() => {
        if (crawler) {
            setCrawlerURL(crawler.start_url);
            setCrawlerName(crawler.name);
        }
    }, [crawler]);

    useStep("crawler-details");

    // SSE for real-time updates
    const { data: sseData, isConnected, error: sseError } = useCrawlerSSE(crawlerId);

    useEffect(() => {
        if (!sseData) return;
        
        switch (sseData.type) {
            case 'crawl_job_update':
                setCrawlerList(crawlerList => crawlerList.map(c => mergeCrawler(c, sseData)));
                break;
                
            case 'error':
                console.error('SSE Error:', sseData.message);
                break;
        }
    }, [setCrawlerList, sseData]);

    if (!crawler) {
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

        {/* Real-time status */}
        <Box sx={{ mb: 2 }}>
            <Chip 
                label={isConnected ? "Live-Updates aktiv" : "Verbindung getrennt"} 
                color={isConnected ? "success" : "error"}
                sx={{ mr: 1 }}
            />
            {sseError && (
                <Chip 
                    label={`Fehler: ${sseError}`} 
                    color="error"
                    sx={{ mr: 1 }}
                />
            )}
        </Box>

        <h2>Läufe des Crawlers</h2>

        <TableContainer component={Paper}>
        <Table>
            <TableHead>
                <TableRow>
                    <TableCell>Start URL</TableCell>
                    <TableCell>Gecrawlte URLs</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Erstellt</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {crawler.crawl_jobs.map(job => (
                    <TableRow key={job.id}>
                        <TableCell>{job.start_url}</TableCell>
                        <TableCell>{job.crawled_url_count || '-'}</TableCell>
                        <TableCell>
                            <Chip 
                                label={job.state} 
                                color={
                                    job.state?.toUpperCase() === 'RUNNING' ? 'primary' :
                                    job.state?.toUpperCase() === 'COMPLETED' ? 'success' :
                                    job.state?.toUpperCase() === 'FAILED' ? 'error' :
                                    'default'
                                }
                                size="small"
                            />
                        </TableCell>
                        <TableCell>{toRelativeDate(job.created_at)}</TableCell>
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

function toRelativeDate(isoTimestamp: string) {
    if (!isoTimestamp) return '-';
    const result = DateTime.fromISO(isoTimestamp).toRelative();
    if (result === 'vor 1 Tag') return 'Vor einem Tag';
    if (result === 'vor 1 Stunde') return 'Vor einer Stunde';
    return result || '-';
}
