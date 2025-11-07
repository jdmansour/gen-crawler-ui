import Delete from '@mui/icons-material/Delete';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Paper from '@mui/material/Paper';
import Switch from '@mui/material/Switch';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { Stack } from "@mui/system";
import {
  getMRT_RowSelectionHandler,
  MaterialReactTable,
  MRT_RowSelectionState,
  useMaterialReactTable,
  type MRT_ColumnDef
} from 'material-react-table';
import { useEffect, useMemo, useState } from "react";
import { createPortal } from "react-dom";
import { EvaluateFiltersResult } from './apitypes';
import { Rule, UnmatchedResponse } from "./schema";
import { useStep } from "./steps";


export default function FilterSetPage(props: { filterSetId: number, csrfToken: string }) {
  // type is a json dict
  const [selectedRuleDetails, setSelectedRuleDetails] = useState({});
  const [unmatchedUrls, setUnmatchedUrls] = useState<UnmatchedResponse | null>(null);
  const [rowSelection, setRowSelection] = useState<MRT_RowSelectionState>({});
  const [evaluationResult, setEvaluationResult] = useState<EvaluateFiltersResult>({ id: 0, remaining_urls: 0, name: "", created_at: "", updated_at: "", rules: [] });
  const crawlJobId = 14;  // TODO: make dynamic

  const apiBase = "http://localhost:8000/api";
  const filterSetId = props.filterSetId;
  useStep('filters')

  async function evaluateFilters() {
    const url = apiBase + `/crawl_jobs/${crawlJobId}/evaluate_filters/`;
    // POST
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': props.csrfToken,
      },
      body: JSON.stringify({ rules: selectedRuleDetails }),
    });
    const data: EvaluateFiltersResult = await response.json();
    console.log(data);
    setEvaluationResult(data);
  }
  
  useEffect(() => {
    evaluateFilters();
    fetchUnmatchedUrls();
  }, [filterSetId]);

  async function fetchUnmatchedUrls() {
    const url = apiBase + `/filter_sets/${filterSetId}/unmatched?crawl_job=${crawlJobId}`;
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);
    setUnmatchedUrls(data);
  }

  async function deleteRow(id: number) {
    console.log("delete", id);

    const response = await fetch(`${apiBase}/filter_rules/${id}/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': props.csrfToken,
      },
    });
    const data = await response.json();
    console.log(data);

    //setRules(rules.filter((rule) => rule.id !== id));
    setEvaluationResult({ ...evaluationResult, rules: evaluationResult.rules.filter((rule) => rule.id !== id) });
  }

  async function addRowAfter(id: number) {
    console.log("add after", id);
    const filterSetUrl = apiBase + `/filter_sets/${filterSetId}/`;
    console.log("filterSetUrl", filterSetUrl);
    const newRule = {
      // TODO: how to make it so we can use an ID and not a URL?
      "filter_set": filterSetUrl,
      //"filter_set": "1",
      "rule": "https://www.weltderphysik.de/wir",
      "count": 123,
      "include": true,
      "page_type": "New row"
    }
    //setRules([...rules, newRule]);
    // insert after rule with the id
    const post_url = apiBase + "/filter_rules/";
    const response = await fetch(post_url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': props.csrfToken,
      },
      body: JSON.stringify(newRule),
    });
    const data = await response.json();
    console.log(data);
    // TODO: add ordering
    //setRules([...rules, data]);
    setEvaluationResult({ ...evaluationResult, rules: [...evaluationResult.rules, data] });
  }

  async function addRowWithDataAfter(id: number, ruleData: { rule: string }): Promise<Rule> {
    console.log("add after", id);
    const filterSetUrl = apiBase + `/filter_sets/${filterSetId}/`;
    console.log("filterSetUrl", filterSetUrl);
    const newRule = {
      // TODO: how to make it so we can use an ID and not a URL?
      "filter_set": filterSetUrl,
      //"filter_set": "1",
      "rule": ruleData.rule,
      "count": 666,
      "include": true,
      "page_type": "New row"
    }
    //setRules([...rules, newRule]);
    // insert after rule with the id
    const post_url = apiBase + "/filter_rules/";
    const response = await fetch(post_url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': props.csrfToken,
      },
      body: JSON.stringify(newRule),
    });
    const data = await response.json();
    console.log(data);
    // TODO: add ordering
    //setRules([...rules, data]);
    setEvaluationResult({ ...evaluationResult, rules: [...evaluationResult.rules, data] });
    return data;
  }

  async function updateFields(id: number, fields: { rule?: string, include?: boolean, page_type?: string }) {
    // Update the fields in the row right away
    // TODO: add a "pending" field to the row, so we can see that the update is in progress
    const newRules1 = evaluationResult.rules.map((rule) => (rule.id === id) ? { ...rule, ...fields } : rule);
    setEvaluationResult({ ...evaluationResult, rules: newRules1 });

    // // sleep 2 seconds to simulate a bad connection
    // await new Promise(r => setTimeout(r, 2000));

    // call the api
    const url = `${apiBase}/filter_rules/${id}/`;
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': props.csrfToken,
      },
      // The field names are the same as in the JSON schema,
      // so we can just pass this object here.
      // Typescript hopefully ensures that we don't pass any other fields.
      body: JSON.stringify(fields),
    });
    const updatedRule = await response.json();
    console.log(updatedRule);

    // actually we should refresh everything to get the new match counts
    await evaluateFilters();
    await fetchUnmatchedUrls();
  }

  function moveDelta(delta: number) {
    return async (id: number) => {
      // construct the url
      const url = `${apiBase}/filter_rules/${id}/`;
      // call the api
      const old_position = evaluationResult.rules.find((rule) => rule.id === id)?.position;
      if (old_position === undefined) {
        console.error("Could not find position of rule with id", id);
        return;
      }
      const response = await fetch(url, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': props.csrfToken,
        },
        body: JSON.stringify({ position: old_position + delta }),
      });
      const updatedRule = await response.json();
      console.log(updatedRule);
      await evaluateFilters();
    }
  }

  async function showDetails(id: number) {
    console.log("show details", id);
    setSelectedRuleDetails({});
    // fetch the details
    const url = `${apiBase}/filter_rules/${id}/matches/?crawl_job=${crawlJobId}`;
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);
    setSelectedRuleDetails(data);
  }

  useEffect(() => {
    console.log("rowSelection changed", rowSelection);
    const selectedRowId = Object.keys(rowSelection)[0];
    // get the row object (rule)
    const selectedRow = evaluationResult.rules.find((rule) => rule.id === Number(selectedRowId));
    if (selectedRow) {
      showDetails(Number(selectedRowId));
    }
  }, [rowSelection, evaluationResult.rules]);

  const selectedFilterRule = useMemo(() => {
    const selectedRowId = Object.keys(rowSelection)[0];
    if (selectedRowId) {
      return evaluationResult.rules.find((rule) => rule.id === Number(selectedRowId));
    }
  }, [rowSelection, evaluationResult.rules]);

  let detailUrls: string[];
  // selectedRuleDetails['new_matches'];
  if (selectedRuleDetails['new_matches'] !== undefined) {
    detailUrls = selectedRuleDetails['new_matches'];
  } else {
    detailUrls = [];
  }

  const lastId = Math.max(...evaluationResult.rules.map(r => r.id), 0);

  const rows = evaluationResult.rules;
  const columns: MRT_ColumnDef<Rule>[] = [
    {
      accessorKey: 'rule',
      header: 'URL-Muster',
      size: 300,
      enableEditing: true,
      muiEditTextFieldProps: ({ cell, column, row, table }) => ({
        variant: "standard",
        fullWidth: true,
        slotProps: {
          input: { sx: { fontSize: 'inherit', m: -0, height: 22, marginTop: "2px", marginBottom: "-2px" } }
        },
        onBlur: async (event) => {
          // table.setEditingCell(null) is called automatically onBlur internally
          console.log("onBlur called");
          console.log('table.getState().creatingRow', table.getState().creatingRow);
          if (table.getState().creatingRow) {
            console.log("Submitting new row");
            const data = await addRowWithDataAfter(lastId, { rule: event.target.value });
            console.log("data returned from addRowWithDataAfter", data);

            row._valuesCache[column.id] = event.target.value;
            row._valuesCache['id'] = data.id;
            row._valuesCache['count'] = data.count;
            row._valuesCache['cumulative_count'] = data.cumulative_count;
            table.setCreatingRow(row);
          } else {
            updateFields(row.original.id, { rule: event.target.value });
          }
        },
        // Make double click work properly: Don't select the whole text, but only the word under the cursor
        onDoubleClick: (event) => event.stopPropagation(),
        // onKeyDown: (event) => {
        //   if (event.key === 'Enter' && table.getState().creatingRow) {
        //     event.preventDefault();
        //     const rule = (event.target as HTMLInputElement).value;
        //     addRowWithDataAfter(lastId, {rule});
        //     table.setCreatingRow(null);
        //   }
        // },
      }),
    },
    {
      accessorKey: 'count',
      header: 'Treffer',
      size: 10,
      enableEditing: false,
    },
    {
      accessorKey: 'cumulative_count',
      header: 'Neue Treffer',
      size: 10,
      enableEditing: false,
    },
    {
      accessorKey: 'include',
      header: 'Behalten',
      size: 10,
      enableEditing: false,
      Cell: ({ cell }) => <Switch checked={Boolean(cell.getValue())} sx={{ m: -1 }}
        onChange={(e) => {
          const row = cell.row.original;
          updateFields(row.id, { include: e.target.checked });
        }} />,
    },
    // {
    //   accessorKey: 'position',
    //   header: 'Position',
    //   size: 10,
    //   enableEditing: false,
    // },
    // {
    //   accessorKey: 'id',
    //   header: 'Id',
    //   size: 10,
    //   enableEditing: false,
    // },
  ];



  const table = useMaterialReactTable({
    enableDensityToggle: true,
    enableFullScreenToggle: false,
    enableColumnActions: false,
    enableColumnFilters: false,
    enableSorting: false,
    enableHiding: false,
    enableTopToolbar: false,
    enableGlobalFilter: false,
    enableRowOrdering: true,
    enablePagination: false,
    enableEditing: true,
    enableRowActions: true,
    positionActionsColumn: 'last',
    renderRowActions: ({ row, table }) => (
      <IconButton onClick={() => console.info('Delete')}>
        <Delete onClick={() => {
          const id = row.original.id;
          deleteRow(row.original.id);
          setEvaluationResult({ ...evaluationResult, rules: evaluationResult.rules.filter((rule) => rule.id !== id) });
        }} />
      </IconButton>
    ),
    editDisplayMode: 'cell',
    enableMultiRowSelection: false, //shows radio buttons instead of checkboxes
    enableRowSelection: true,
    initialState: {
      density: 'comfortable',
      columnVisibility: {
        'mrt-row-select': false,
      },
    },
    columns,
    data: rows,
    // layoutMode: 'grid',
    displayColumnDefOptions: {
      'mrt-row-drag': {
        header: '',
        grow: 0,
        size: 10
      },
      'mrt-row-actions': {
        header: '',
        grow: 0,
        size: 10
      }
    },
    onRowSelectionChange: setRowSelection,
    state: { rowSelection },
    getRowId: (originalRow) => String(originalRow.id),
    muiTableBodyRowProps: ({ row, staticRowIndex, table }) => ({
      // hover: true,
      // sx: {
      //   transition: 'all 150ms ease-in-out',
      //   backgroundColor: row.original.include ? 'hsl(0, 0%, 100%)' : 'hsl(354, 83%, 93%)',
      //   '&:hover': {
      //     transition: 'all 0ms linear',
      //     // remove grey shading on hover
      //     backgroundColor: 'transparent',
      //     '&.MuiTableRow-hover': {
      //       backgroundColor: row.original.include ? 'hsl(0, 0%, 95%)' : 'hsl(354, 83%, 90%)',
      //       'td::after': {
      //         // remove other grey shading on td::after on hover
      //         backgroundColor: 'transparent',
      //       },
      //     },
      //   },
      // },
      // single click to select row
      onClick: (event) =>
        getMRT_RowSelectionHandler({ row, staticRowIndex, table })(event), //import this helper function from material-react-table
    }),
    // muiTableBodyCellProps: ({ cell, column, table }) => ({
    // // Single-click to edit
    // onClick: () => {
    //   table.setEditingCell(cell); //set editing cell
    //   //optionally, focus the text field
    //   queueMicrotask(() => {
    //     const textField = table.refs.editInputRefs.current?.[column.id];
    //     if (textField) {
    //       textField.focus();
    //       textField.select?.();
    //     }
    //   });
    // },
    // }),
    muiTableBodyProps: {
      sx: {
        '--col-mrt_row_drag-size': '20px',
        '--header-mrt_row_drag-size': '20px',
        '--col-mrt_row_actions-size': '20px',
        '--header-mrt_row_actions-size': '20px',
      },
    },
    muiTableHeadCellProps: ({ column }) => ({
      sx: {
        // // fontWeight: 'bold',
        // // fontSize: '0.9rem',
        // // align center for position and actions columns
        // '> div': {
        //   justifyContent: (column.id === 'mrt-row-drag' || column.id === 'mrt-row-actions') ? 'center' : 'flex-start',
        // },
        // // textAlign: (column.id === 'mrt-row-drag' || column.id === 'mrt-row-actions') ? 'center' : 'left',
        paddingLeft: column.id === 'mrt-row-drag' ? 2 : column.id === 'mrt-row-actions' ? 0 : 1,
        paddingRight: column.id === 'mrt-row-drag' ? 0 : column.id === 'mrt-row-actions' ? 0 : 1,
        // width: column.id === 'mrt-row-drag' ? '0' : undefined,
        // minWidth: 'auto',
        boxSizing: 'border-box',
        // maxWidth: 'initial', //column.id === 'mrt-row-drag' ? 10 : 'none',
      },
    }),
    muiTableBodyCellProps: ({ cell, column, table }) => ({
      // adjust padding for cells in the position and actions columns
      sx: {
        // // textAlign: (column.id === 'mrt-row-drag'  ? 'center' : 'left',
        paddingLeft: column.id === 'mrt-row-drag' ? 2 : column.id === 'mrt-row-actions' ? 0 : 1,
        paddingRight: column.id === 'mrt-row-drag' ? 0 : column.id === 'mrt-row-actions' ? 0 : 1,
        // width: column.id === 'mrt-row-drag' ? '0' : undefined,
        // minWidth: 'auto',
        boxSizing: 'border-box',
        // maxWidth: column.id === 'mrt-row-drag' || column.id === 'mrt-row-actions' ? 10 : 'none',
      },
    }),
    positionToolbarAlertBanner: 'none',
    createDisplayMode: 'row',
    positionCreatingRow: 'bottom',
    renderBottomToolbarCustomActions: ({ table }) => (
      <Button variant="contained" onClick={() => table.setCreatingRow(true)}>Regel hinzufügen</Button>
    ),
    // onCreatingRowCancel: () => setValidationErrors({}),
    onCreatingRowSave: ({ row, table, values }) => {
      console.log("Creating row", { row, table, values });
      addRowWithDataAfter(lastId, values);
      table.setCreatingRow(null);
    },
    enableStickyHeader: true,
    enableStickyFooter: true,
    muiTableContainerProps: {
      sx: {
        maxHeight: '100%', // take all available height
        overflowY: 'overlay', // enable vertical scroll
        // overflowX: 'clip',
      },
    }
  });

  const sidebarOutlet = document.getElementById("sidebar-outlet");

  return (
    <>
      {/* <p>{filterSet?.crawl_job.crawled_url_count} pages total, {filterSet?.remaining_urls} not handled yet</p> */}
      <h3>Rules</h3>

      <p>Data from crawl job {crawlJobId}</p>

      <MaterialReactTable table={table} />

      <Stack direction="row" spacing={2} sx={{ mt: 2, mb: 2 }}>
        <Button variant="outlined" sx={{ textTransform: 'none' }}>Regel hinzufügen</Button>
        <Button variant='outlined' sx={{ textTransform: 'none' }} onClick={evaluateFilters}>Filter auswerten</Button>
        <Button variant="contained" style={{ textTransform: 'none', marginLeft: 'auto' }}>Start content crawl</Button>
      </Stack>

      {sidebarOutlet && createPortal(
        <FilterSetPageSidebar
          selectedFilterRule={selectedFilterRule}
          detailUrls={selectedFilterRule ? detailUrls : unmatchedUrls?.unmatched_urls || []} />,
        sidebarOutlet
      )}
    </>
  );
}

function FilterSetPageSidebar(props: { selectedFilterRule?: Rule, detailUrls: string[] }) {
  const { selectedFilterRule, detailUrls } = props;
  return <div>
    <div style={{ position: 'sticky' }}>
      <h3>Details</h3>

      <p>Ausgewählter Filter:</p>
      <p>Regel: <code>{selectedFilterRule?.rule}</code></p>
      <p>Treffer: <code>{selectedFilterRule?.count}</code></p>
      <p>Davon nicht durch vorherige Regeln erfasst: <code>{selectedFilterRule?.cumulative_count}</code></p>
    </div>

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
