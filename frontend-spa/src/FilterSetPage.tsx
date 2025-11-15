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
import { JSX, useCallback, useEffect, useMemo, useState } from "react";
import { createPortal } from "react-dom";
import { EvaluateFiltersResult, RuleEvaluation } from './apitypes';
import { Rule, UnmatchedResponse } from "./schema";
import { useStep } from "./steps";
import { useOutletContext, useParams } from 'react-router';
import { FilterSetPageContext } from './RootContext';
import { Skeleton } from '@mui/material';


const apiBase = "http://localhost:8000/api";

export default function FilterSetPage(props: { csrfToken: string }) {
  // type is a json dict
  const [rowSelection, setRowSelection] = useState<MRT_RowSelectionState>({});
  const [evaluationResult, setEvaluationResult] = useState<EvaluateFiltersResult>({ id: 0, remaining_urls: 0, name: "", created_at: "", updated_at: "", rules: [] });
  const { crawlerList, crawlerListLoaded } = useOutletContext<FilterSetPageContext>();
  // const crawlJobId = 14;  // TODO: make dynamic
  const { crawlerId } = useParams();

  const crawler = crawlerList.find(c => c.id === Number(crawlerId));

  // // get crawler from crawlerList matching filterSetId
  // const crawler = crawlerList.find(c => c.filter_set_id === props.filterSetId);
  // pick the crawl job with the latest updated_at
  const crawlJob = crawler?.crawl_jobs.reduce((latest, job) => {
    return new Date(job.updated_at) > new Date(latest.updated_at) ? job : latest;
  }, crawler.crawl_jobs[0]);

  // todo: handle case where crawler or crawlJob is undefined
  const crawlJobId = crawlJob?.id;
  const filterSetId = crawler?.filter_set_id;
  // const filterSetId = props.filterSetId;
  console.log("FilterSetPage crawlerId", crawlerId, "crawlJobId", crawlJobId, "filterSetId", filterSetId);
  console.log("crawlerList.length", crawlerList.length);
  useStep('filters')

  const evaluateFilters = useCallback(async () => {
    const url = apiBase + `/crawl_jobs/${crawlJobId}/evaluate_filters/`;
    // POST
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': props.csrfToken,
      },
      body: JSON.stringify({}),
    });
    if (!response.ok) {
      console.error("Failed to evaluate filters");
      return;
    }
    const data: EvaluateFiltersResult = await response.json();
    setEvaluationResult(data);
  }, [crawlJobId, props.csrfToken]);
  
  useEffect(() => {
    evaluateFilters();
  }, [evaluateFilters]);


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
  }

  const selectedFilterRule = useMemo(() => {
    const selectedRowId = Object.keys(rowSelection)[0];
    if (selectedRowId) {
      return evaluationResult.rules.find((rule) => rule.id === Number(selectedRowId));
    }
  }, [rowSelection, evaluationResult.rules]);

  const lastId = Math.max(...evaluationResult.rules.map(r => r.id), 0);
  const lastPosition = Math.max(...evaluationResult.rules.map(r => r.position), 0);

  const sortedRows = evaluationResult.rules.sort((a, b) => a.position - b.position)
  const lastRow: Rule = {
    'id': -1,
    'position': lastPosition + 1,
    'rule': '<Nicht erfasst>',
    'count': 0,
    'cumulative_count': evaluationResult.remaining_urls,
    'include': true,
    'page_type': '',
  };
  const rows = [...sortedRows, lastRow];
  const columns: MRT_ColumnDef<Rule>[] = [
    {
      accessorKey: 'rule',
      header: 'URL-Muster',
      size: 300,
      enableEditing: (row) => row.original.id !== -1,
      muiEditTextFieldProps: ({ column, row, table }) => ({
        variant: "standard",
        fullWidth: true,
        slotProps: {
          input: { sx: { fontSize: 'inherit', m: -0, height: 22, marginTop: "2px", marginBottom: "-2px" } }
        },
        onBlur: async (event) => {
          // table.setEditingCell(null) is called automatically onBlur internally
          console.log("onBlur called");
          console.log('table.getState().creatingRow', table.getState().creatingRow);
          // TODO: this is broken and needs fixing!
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
      accessorFn: (row: Rule): string => row.id === -1 ? '' : String(row.count),
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
      Cell: ({ cell }) => <Switch
        checked={Boolean(cell.getValue())}
        sx={{ m: -1, visibility: cell.row.original.id === -1 ? 'hidden' : 'visible' }}
        onChange={(e) => {
          const row = cell.row.original;
          updateFields(row.id, { include: e.target.checked });
        }} />,
    },
    {
      accessorKey: 'position',
      header: 'Position',
      size: 10,
      enableEditing: false,
    },
    {
      accessorKey: 'id',
      header: 'Id',
      size: 10,
      enableEditing: false,
    },
  ];



  const table = useMaterialReactTable({
    enableDensityToggle: true,
    enableFullScreenToggle: false,
    enableColumnActions: false,
    enableColumnFilters: false,
    enableSorting: false,
    enableHiding: false,
    enableTopToolbar: false,
    enableBottomToolbar: false,
    enableGlobalFilter: false,
    enableRowOrdering: true,
    muiRowDragHandleProps: ({ row, table }) => ({
      sx: { visibility: row.original.id === -1 ? 'hidden' : 'visible', cursor: 'grab' },
      onDragEnd: async () => {
        const { draggingRow, hoveredRow } = table.getState();

        if (!(hoveredRow && draggingRow)) {
          return;
        }

        const hoveredPosition = hoveredRow.original!.position;
        const draggedId = draggingRow.original!.id;

        const url = `${apiBase}/filter_rules/${draggedId}/`;
        // call PATCH and update position to the position of where it was dropped
        const response = await fetch(url, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': props.csrfToken,
          },
          body: JSON.stringify({ position: hoveredPosition }),
        });
        const data = await response.json();
        console.log("Move response", data);

        // Update local state so we get immediate feedback
        // const newRules = moveRule(evaluationResult.rules, draggedId, hoveredPosition);
        // for (let i = 0; i < newRules.length; i++) {
        //   console.log("Moving rule", newRules[i].id, "from", evaluationResult.rules[i].position, "to", newRules[i].position);
        // }
        // setEvaluationResult({ ...evaluationResult, rules: newRules });
        setEvaluationResult(prev => ({ ...prev, rules: moveRule(prev.rules, draggedId, hoveredPosition) }));

        // re-evaluate filters to get updated counts
        await evaluateFilters();
      },
    }),
    enablePagination: false,
    enableEditing: true,
    enableRowActions: true,
    positionActionsColumn: 'last',
    renderRowActions: ({ row }) => (
      (row.original.id !== -1) && (
        <IconButton onClick={() => console.info('Delete')}>
          <Delete onClick={() => {
            const id = row.original.id;
            deleteRow(row.original.id);
            setEvaluationResult({ ...evaluationResult, rules: evaluationResult.rules.filter((rule) => rule.id !== id) });
        }} />
      </IconButton>)
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
    muiTableBodyCellProps: ({ column }) => ({
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
    positionCreatingRow: rows.length-1,
    // renderBottomToolbarCustomActions: ({ table }) => (
    //   <Button variant="contained" onClick={() => table.setCreatingRow(true)}>Regel hinzufügen</Button>
    // ),
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
      },
    },
    muiTablePaperProps: {
      sx: {
        flexBasis: 'auto',
        // flexGrow: 1
        flexShrink: 1,
      },
    },
  });

  const sidebarOutlet = document.getElementById("sidebar-outlet");

  let content: JSX.Element;
  if (!crawlerListLoaded) {
    content = <Skeleton variant="rounded" animation="wave" width={"100%"} height={200} />;
  } else if (filterSetId === undefined || filterSetId === null) {
    content = <div>Fehler: Kein filter_set gefunden</div>;
  } else if (crawlJobId === undefined || crawlJobId === null) {
    content = <div>Fehler: Kein crawl job gefunden</div>;
  } else {
    content = <>
      <MaterialReactTable table={table} />

      <Stack direction="row" spacing={2} sx={{ mt: 1 }}>
        <Button variant="outlined" sx={{ textTransform: 'none' }} onClick={() => table.setCreatingRow(true)}>Regel hinzufügen</Button>
        <Button variant='outlined' sx={{ textTransform: 'none' }} onClick={evaluateFilters}>Filter auswerten</Button>
        <Button variant="contained" style={{ textTransform: 'none', marginLeft: 'auto' }}>Start content crawl</Button>
      </Stack>
    </>;
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", flex: 1,
                        padding: "8px 24px 16px 24px", gap: "16px", flexShrink: 1, minHeight: 350}}>
      <h2 style={{ margin: "0px 0px" }}>Filterregeln</h2>

      <div><a href={`http://localhost:8000/admin/crawls/filterset/${filterSetId}/change/`}>Filter set {filterSetId}</a></div>
      <div><a href={`http://localhost:8000/admin/crawls/crawljob/${crawlJobId}/change/`}>Data from crawl job {crawlJobId}</a></div>
      <div>Crawler list loaded: {crawlerListLoaded ? "Yes" : "No"}</div>

      {content}

      {sidebarOutlet && createPortal(
        <FilterSetPageSidebar
          filterSetId={filterSetId || null}
          crawlJobId={crawlJobId || null}
          selectedFilterRule={selectedFilterRule} />,
        sidebarOutlet
      )}
    </div>
  );
}

function FilterSetPageSidebar(props: {
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
    <div style={{ position: 'sticky' }}>
      <h3>Details</h3>

      {selectedFilterRuleId ? (
      <><p>Ausgewählter Filter:</p><p>Regel: <code>{selectedFilterRule?.rule}</code></p><p>Treffer: <code>{selectedFilterRule?.count}</code></p><p>Davon nicht durch vorherige Regeln erfasst: <code>{selectedFilterRule?.cumulative_count}</code></p></>
      ) : (
      <p>URLs, die durch keine Regel erfasst wurden:</p>
      )}
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

function moveRule(rules: RuleEvaluation[], id: number, toPosition: number) {
  // this mirrors move_to in models.py
  // Move rule id to toPosition, shifting other rules as necessary.
  // If the target position is already taken, increase the position of all rules
  // above or equal to toPosition by 1.

  console.log("moveRule moving id", id, "to position:", toPosition);

  // const rules = evaluationResult.rules;
  const rule = rules.find((r) => r.id === id);
  if (!rule) {
    return rules;
  }

  if (rule.position == toPosition) {
    // notihing to do
    return rules;
  }

  const clamp = (num: number, min: number, max: number): number => Math.min(Math.max(num, min), max);
  const newPosition = clamp(toPosition, 1, rules.length);
  const curPosition = rule.position;
  if (newPosition > curPosition) {
    // moving down
    const newRules = rules.map((r) => {
      if (r.id === id) {
        return { ...r, position: newPosition };
      }
      if (r.position > curPosition && r.position <= newPosition) {
        return { ...r, position: r.position - 1 };
      }
      return r;
    });
    return newRules;
  } else {
    // moving up
    const newRules = rules.map((r) => {
      if (r.id === id) {
        return { ...r, position: newPosition };
      }
      if (r.position >= newPosition && r.position < curPosition) {
        return { ...r, position: r.position + 1 };
      }
      return r;
    });
    return newRules;
  }
}