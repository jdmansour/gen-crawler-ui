import Cancel from '@mui/icons-material/Cancel';
import Delete from '@mui/icons-material/Delete';
import MoreVertOutlined from "@mui/icons-material/MoreVertOutlined";
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TextField from '@mui/material/TextField';
import { Stack } from '@mui/system';
import { DateTime } from "luxon";
import { useEffect, useState } from "react";
import { Link, useOutletContext, useParams } from "react-router-dom";
import { Crawler, CrawlJob, SourceItem } from "./apitypes";
import sourcePreviewPic from "./assets/source-preview.jpg";
import DeleteCrawlerDialog from './DeleteCrawlerDialog';
import { useCrawlerSSE } from "./hooks/useSSE";
import { CrawlerDetailsContext, CrawlerDetailsPageContext } from "./RootContext";
import { useStep } from "./steps";
import Api from './api';


export default function CrawlerDetailsPage() {
    const { crawlerId } = useParams();
    const { crawlerList, sourceItems } = useOutletContext<CrawlerDetailsPageContext>();
    const { onCrawlJobAdded, onCrawlJobDeleted, onCrawlJobLiveUpdate } = useOutletContext<CrawlerDetailsPageContext>();
    return <CrawlerDetails
        crawlerId={crawlerId ? parseInt(crawlerId) : 0}
        crawlerList={crawlerList}
        sourceItems={sourceItems}
        onCrawlJobAdded={onCrawlJobAdded}
        onCrawlJobDeleted={onCrawlJobDeleted}
        onCrawlJobLiveUpdate={onCrawlJobLiveUpdate}
    />; 
}

export function CrawlerDetails(params: {crawlerId: number, crawlerList: Crawler[], sourceItems: SourceItem[], onCrawlJobAdded: (newJob: CrawlJob) => void, onCrawlJobDeleted: (crawlJobId: number) => void, onCrawlJobLiveUpdate: (sseData: SSEData) => void}) {
    // todo: move onCrawlerDeleted from a param to context?
    const { crawlerId, crawlerList, sourceItems, onCrawlJobAdded, onCrawlJobDeleted, onCrawlJobLiveUpdate } = params;
    const { deleteCrawler } = useOutletContext<CrawlerDetailsContext>();
    const crawler = crawlerList.find(c => c.id == crawlerId);
    const sourceItem = sourceItems.find(s => s.guid === crawler?.source_item);

    const [crawlerURL, setCrawlerURL] = useState<string>("");
    const [crawlerName, setCrawlerName] = useState<string>("");
    const [confirmDeleteOpen, setConfirmDeleteOpen] = useState(false);
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const [selectedJob, setSelectedJob] = useState<CrawlJob | null>(null);
    const menuOpen = Boolean(anchorEl);

    const api = new Api("http://localhost:8000/api");

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
                onCrawlJobLiveUpdate(sseData);
                break;
                
            case 'error':
                console.error('SSE Error:', sseData.message);
                break;
        }
    }, [onCrawlJobLiveUpdate, sseData]);

    // Callbacks for buttons & menus
    // -----------------------------

    async function startCrawlClicked() {
        if (!crawler) return;
        const newJob = await api.startCrawl(crawler.id);
        // Optimistically add the new job to the list
        onCrawlJobAdded(newJob);
    }

    async function startContentCrawlClicked() {
        if (!crawler) return;
        const response = await api.startContentCrawl(crawler.id);
        console.log("Content crawl started");
        console.log("Response:", response);
    }

    function handleMenuClick(event: React.MouseEvent<HTMLElement>, jobId: number) {
        setAnchorEl(event.currentTarget);
        const job = crawler?.crawl_jobs.find(j => j.id == jobId) || null;
        setSelectedJob(job);
    };

    function handleMenuClose() {
        setAnchorEl(null);
    }

    async function deleteCrawlClicked() {
        handleMenuClose();
        // Delete the selected crawl job
        if (!selectedJob) return;
        await api.deleteCrawlJob(selectedJob.id);
        // Remove the job from the crawler's job list
        onCrawlJobDeleted(selectedJob.id);
    }

    async function cancelCrawlClicked() {
        handleMenuClose();
        // Cancel the selected crawl job
        if (!selectedJob) return;
        await api.cancelCrawlJob(selectedJob.id);
    }

    if (!crawler) {
        return <div className="main-content">
            <p>Crawler not found</p>
        </div>;
    }

    return <div style={{overflowY: "scroll", padding: "0px 24px 24px 24px"}}>
        <h2 style={{marginTop: 8}}>Crawler-Details</h2>
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

        <Stack direction="row" spacing={2} sx={{ marginTop: 2, marginBottom: 2 }}>
            <Button variant="contained" color="primary" onClick={async () => {
                // Save crawler details
            }}>Speichern</Button>
        </Stack>

        <h3>Aktionen</h3>

        <Stack direction="row" spacing={2} sx={{ marginTop: 2, marginBottom: 2, flexWrap: 'wrap' }} useFlexGap>
            <Button variant="outlined" color="primary" onClick={startCrawlClicked}>Crawler starten</Button>
            <Button variant="outlined" onClick={startContentCrawlClicked}>Content Crawl starten</Button>
            <Button variant="outlined" component={Link} to={`/crawlers/${crawler.id}/filters/`}>Filter bearbeiten</Button>
            <Button variant="outlined" component="a" href={api.getAdminUrl(crawler.id)}>Im Admin-Bereich anzeigen</Button>
            <Button variant="outlined" color="error" onClick={() => setConfirmDeleteOpen(true)}>Crawler löschen</Button>
        </Stack>

        <DeleteCrawlerDialog
            open={confirmDeleteOpen}
            onClose={() => setConfirmDeleteOpen(false)} 
            onConfirm={() => { setConfirmDeleteOpen(false); deleteCrawler(crawler.id); }} />
    
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

        <h3>Läufe des Crawlers</h3>

        <TableContainer component={Paper}>
        <Table>
            <TableHead>
                <TableRow>
                    <TableCell>Start URL</TableCell>
                    <TableCell>Gecrawlte URLs</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Erstellt</TableCell>
                    <TableCell></TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {crawler.crawl_jobs.sort((a,b) => compareISODateDesc(a.created_at, b.created_at)).map(job => (
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
                        <TableCell>
                            <IconButton
                                aria-controls={menuOpen ? 'crawler-job-menu' : undefined}
                                aria-haspopup="true"
                                aria-expanded={menuOpen ? 'true' : undefined}
                                onClick={(e) => handleMenuClick(e, job.id)}
                            >
                            <MoreVertOutlined />
                            </IconButton>
                        </TableCell>
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
        <Menu id="crawler-job-menu"
            anchorEl={anchorEl}
            open={menuOpen}
            onClose={handleMenuClose}
            slotProps={{ list: {'aria-labelledby': 'crawler-job-button'}, }}
            anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
            transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        >
            <MenuItem sx={{ color: 'error.main' }} onClick={deleteCrawlClicked}>
                <ListItemIcon sx={{ color: 'error.main' }}><Delete fontSize="small" /></ListItemIcon>
                Crawl löschen
            </MenuItem>
            <MenuItem disabled={selectedJob?.state != 'RUNNING' && selectedJob?.state != 'PENDING'} onClick={cancelCrawlClicked}>
                <ListItemIcon><Cancel fontSize="small" /></ListItemIcon>
                Crawl abbrechen
            </MenuItem>
            <MenuItem disabled={!(selectedJob?.scrapy_job_id)} component="a" href={logUrl(selectedJob)}>
                <ListItemIcon><MoreVertOutlined fontSize="small" /></ListItemIcon>
                Show logs
            </MenuItem>
        </Menu>

    </div>;
}

// Gets the scrapy log URL for a crawl job
function logUrl(crawlJob: CrawlJob | null): string {
    if (!crawlJob?.scrapy_job_id) return "";
    return `http://localhost:6800/logs/scraper/example/${crawlJob.scrapy_job_id}.log`;
}

// comparer for two iso date strings
function compareISODateDesc(a: string, b: string) {
    const dateA = new Date(a);
    const dateB = new Date(b);
    return dateB.getTime() - dateA.getTime();
}

// Makes a relative date string from an ISO timestamp
function toRelativeDate(isoTimestamp: string) {
    if (!isoTimestamp) return '-';
    const result = DateTime.fromISO(isoTimestamp).toRelative();
    if (result === 'vor 1 Tag') return 'Vor einem Tag';
    if (result === 'vor 1 Stunde') return 'Vor einer Stunde';
    return result || '-';
}
