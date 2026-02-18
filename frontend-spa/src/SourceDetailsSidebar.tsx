import Chip from "@mui/material/Chip";
import CircularProgress from "@mui/material/CircularProgress";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Typography from "@mui/material/Typography";
import { DateTime } from "luxon";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Api from "./api";
import { Crawler, SimpleState, SourceItem } from "./apitypes";
import { useApiUrl } from "./ApiUrlContext";
import SourceCard from "./SourceCard";

const simpleStateLabels: { [key in SimpleState]: string } = {
  draft: "Entwurf",
  running: "Läuft",
  idle: "Bereit",
  error: "Fehler",
};

const simpleStateColors: { [key in SimpleState]: "default" | "primary" | "success" | "error" } = {
  draft: "default",
  running: "primary",
  idle: "success",
  error: "error",
};

interface SourceDetailsSidebarProps {
  sourceGuid: string;
  /** Pre-loaded source item — if provided, skips fetching */
  sourceItem?: SourceItem;
  /** Pre-loaded crawlers — if provided, skips fetching and filters by sourceGuid */
  crawlers?: Crawler[];
}

export default function SourceDetailsSidebar({ sourceGuid, sourceItem: sourceItemProp, crawlers: crawlersProp }: SourceDetailsSidebarProps) {
  const apiUrl = useApiUrl();
  const [sourceItem, setSourceItem] = useState<SourceItem | undefined>(sourceItemProp);
  const [crawlers, setCrawlers] = useState<Crawler[] | undefined>(
    crawlersProp?.filter(c => c.source_item === sourceGuid)
  );
  const [loading, setLoading] = useState(!sourceItemProp || !crawlersProp);

  useEffect(() => {
    if (sourceItemProp && crawlersProp) return;

    const api = new Api(apiUrl);
    const fetches: Promise<void>[] = [];

    if (!sourceItemProp) {
      fetches.push(
        api.getSourceItem(sourceGuid).then(setSourceItem)
      );
    }

    if (!crawlersProp) {
      fetches.push(
        api.listCrawlers().then(all => {
          setCrawlers(all.filter(c => c.source_item === sourceGuid));
        })
      );
    }

    setLoading(true);
    Promise.all(fetches).finally(() => setLoading(false));
  }, [sourceGuid, apiUrl, sourceItemProp, crawlersProp]);

  if (loading) {
    return (
      <Stack alignItems="center" justifyContent="center" sx={{ p: 4 }}>
        <CircularProgress />
      </Stack>
    );
  }

  return (
    <Stack spacing={2} sx={{ p: 2 }}>
      <SourceCard sourceItem={sourceItem} orientation="horizontal" />

      <Typography variant="h6">Crawler</Typography>

      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Start-URL</TableCell>
            <TableCell>Aktualisiert</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {crawlers && crawlers.length > 0 ? (
            crawlers.map(crawler => (
              <TableRow key={crawler.id} hover>
                <TableCell>
                  <Link to={`/crawlers/${crawler.id}`} style={{ textDecoration: "none", color: "inherit", fontWeight: 600 }}>
                    {crawler.name}
                  </Link>
                </TableCell>
                <TableCell>
                  <Chip
                    label={simpleStateLabels[crawler.simple_state]}
                    color={simpleStateColors[crawler.simple_state]}
                    size="small"
                  />
                </TableCell>
                <TableCell sx={{ maxWidth: 180, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {crawler.start_url}
                </TableCell>
                <TableCell sx={{ whiteSpace: "nowrap" }}>
                  {DateTime.fromISO(crawler.updated_at).toRelative()}
                </TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={4} align="center" sx={{ color: "text.secondary" }}>
                Keine Crawler für diese Quelle
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </Stack>
  );
}
