import { Paper, Tab, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Chip, Box } from "@mui/material";
import { useState, useEffect } from "react";
import { useOutletContext, useParams } from "react-router-dom";
import sourcePreviewPic from "./assets/source-preview.jpg";
import { CrawlerDetailsPageContext } from "./RootContext";
import { useStep } from "./steps";
import { useCrawlerSSE } from "./hooks/useSSE";


export default function CrawlerDetailsPage() {
    const { crawlerId } = useParams();
    const { crawlerList, sourceItems } = useOutletContext<CrawlerDetailsPageContext>();
    const crawler = crawlerList.find(c => c.id.toString() === crawlerId);
    const sourceItem = sourceItems.find(s => s.guid === crawler?.source_item);

    const [crawlerURL, setCrawlerURL] = useState<string>(crawler?.start_url || "");
    const [crawlerName, setCrawlerName] = useState<string>(crawler?.name || "");
    const [realtimeJobs, setRealtimeJobs] = useState(crawler?.crawl_jobs || []);
    const [itemsProcessed, setItemsProcessed] = useState<number>(0);
    const [currentUrl, setCurrentUrl] = useState<string>("");

    useStep("crawler-details");

    // SSE for real-time updates
    const { data: sseData, isConnected, error: sseError } = useCrawlerSSE(crawlerId);

    useEffect(() => {
        if (sseData) {
            console.log('Received SSE data:', sseData);
            
            switch (sseData.type) {
                case 'initial':
                    if (sseData.crawl_jobs) {
                        setRealtimeJobs(sseData.crawl_jobs);
                    }
                    break;
                    
                case 'status_update':
                    // Update the specific crawl job state
                    setRealtimeJobs(prev => 
                        prev.map(job => 
                            job.id === sseData.crawl_job_id 
                                ? { ...job, state: sseData.state || job.state }
                                : job
                        )
                    );
                    break;
                    
                case 'progress_update':
                    if (sseData.items_processed !== undefined) {
                        setItemsProcessed(sseData.items_processed);
                    }
                    if (sseData.current_url) {
                        setCurrentUrl(sseData.current_url);
                    }
                    break;
                    
                case 'error':
                    console.error('SSE Error:', sseData.message);
                    break;
            }
        }
    }, [sseData]);

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

        {/* Real-time status */}
        <Box sx={{ mb: 2 }}>
            <Chip 
                label={isConnected ? "Live-Updates aktiv" : "Verbindung getrennt"} 
                color={isConnected ? "success" : "error"}
                sx={{ mr: 1 }}
            />
            {itemsProcessed > 0 && (
                <Chip 
                    label={`${itemsProcessed} Items verarbeitet`} 
                    color="info"
                    sx={{ mr: 1 }}
                />
            )}
            {sseError && (
                <Chip 
                    label={`Fehler: ${sseError}`} 
                    color="error"
                    sx={{ mr: 1 }}
                />
            )}
        </Box>

        {currentUrl && (
            <Box sx={{ mb: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                <strong>Aktuelle URL:</strong> {currentUrl}
            </Box>
        )}

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
                {realtimeJobs.map(job => (
                    <TableRow key={job.id}>
                        <TableCell>{job.start_url}</TableCell>
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
                        <TableCell>{job.created_at ? new Date(job.created_at).toLocaleString("de-DE") : '-'}</TableCell>
                    </TableRow>
                ))}
                {(realtimeJobs.length === 0) && (
                    <TableRow>
                        <TableCell colSpan={3}>No crawl jobs found.</TableCell>
                    </TableRow>
                )}
            </TableBody>
        </Table>
        </TableContainer>

    </div>;

}