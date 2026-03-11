import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { useEffect, useState } from "react";
import { Rule, UnmatchedResponse } from "./schema";
import { Box } from '@mui/material';
import { SidebarTitle } from "./SiteLayout";

const apiBase = "http://localhost:8000/api";

export default function FilterSetPageSidebar(props: {
  filterSetId: number | null,
  selectedFilterRule?: Rule,
  crawlJobId: number | null,
}) {
  const { selectedFilterRule, filterSetId, crawlJobId } = props;
  const [unmatchedUrls, setUnmatchedUrls] = useState<UnmatchedResponse | null>(null);
  const [selectedRuleDetails, setSelectedRuleDetails] = useState<{ new_matches: string[], other_matches: string[] }>({ new_matches: [], other_matches: [] });
  const selectedFilterRuleId = selectedFilterRule?.id || null;

  async function fetchUnmatchedUrls(filterSetId: number, crawlJobId: number) {
    const url = apiBase + `/filter_sets/${filterSetId}/unmatched/?crawl_job=${crawlJobId}`;
    const response = await fetch(url);
    const data = await response.json();
    setUnmatchedUrls(data);
  }

async function showDetails(selectedFilterRuleId: number, crawlJobId: number) {
    setSelectedRuleDetails({new_matches: [], other_matches: []});
    // fetch the details
    const url = `${apiBase}/filter_rules/${selectedFilterRuleId}/matches/?crawl_job=${crawlJobId}`;
    const response = await fetch(url);
    const data = await response.json();
    setSelectedRuleDetails(data);
  }

  useEffect(() => {
    if (crawlJobId === null || filterSetId === null) {
      return;
    }

    if (selectedFilterRuleId !== undefined && selectedFilterRuleId !== null) {
      showDetails(selectedFilterRuleId, crawlJobId);
    } else {
      if (filterSetId !== undefined) {
        fetchUnmatchedUrls(filterSetId, crawlJobId);
      }
    }
  }, [selectedFilterRuleId, crawlJobId, filterSetId]);


  let detailUrls: string[];
  if (selectedFilterRuleId) {
    // show urls matching this rule
    detailUrls = selectedRuleDetails['new_matches'] || [];
  } else {
    // show unmatched urls
    detailUrls = unmatchedUrls?.unmatched_urls || [];
  }

  return <div>
    <SidebarTitle>Filter Details</SidebarTitle>
    <Box sx={{ px: 3, mb: 2 }}>
      {selectedFilterRuleId ? (
      <><div>Ausgewählter Filter:</div><div>Regel: <code>{selectedFilterRule?.rule}</code></div><div>Treffer: <code>{selectedFilterRule?.count}</code></div><div>Davon nicht durch vorherige Regeln erfasst: <code>{selectedFilterRule?.cumulative_count}</code></div></>
      ) : (
      <div>URLs, die durch keine Regel erfasst wurden:</div>
      )}
    </Box>

    <TableContainer component={Paper}>
      <Table stickyHeader size="small">
        <TableHead>
          <TableRow>
            <TableCell>URL</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {detailUrls.map((url) => (
            <TableRow key={url}>
              <TableCell>
                {url}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  </div>;
}
