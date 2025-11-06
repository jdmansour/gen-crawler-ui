import { Delete } from "@mui/icons-material";
import { Button, IconButton, Paper, Switch, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
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
import { FilterSet, Rule, UnmatchedResponse } from "./schema";
import { useStep } from "./steps";


export default function FilterSetPage(props: { filterSetId: number, csrfToken: string }) {
  const [filterSet, setFilterSet] = useState<FilterSet | null>(null);
  const [rules, setRules] = useState<Rule[]>([]);
  // type is a json dict
  const [selectedRuleDetails, setSelectedRuleDetails] = useState({});
  const [unmatchedUrls, setUnmatchedUrls] = useState<UnmatchedResponse | null>(null);
  const [rowSelection, setRowSelection] = useState<MRT_RowSelectionState>({});

  const apiBase = "http://localhost:8000/api";
  const filterSetId = props.filterSetId;
  // console.log("filterSetId", filterSetId);
  useStep('filters')

  async function fetchData() {
    const url = apiBase + `/filter_sets/${filterSetId}/`;
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);
    setFilterSet(data);
    setRules(data.rules);
  }
  useEffect(() => {
    fetchData();
    fetchUnmatchedUrls();
  }, []);

  async function fetchUnmatchedUrls() {
    const url = apiBase + `/filter_sets/${filterSetId}/unmatched`;
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

    setRules(rules.filter((rule) => rule.id !== id));
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
    setRules([...rules, data]);
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
    setRules([...rules, data]);
    return data;
  }

  async function updateFields(id: number, fields: { rule?: string, include?: boolean, page_type?: string }) {
    // Update the fields in the row right away
    const newRules1 = rules.map((rule) => (rule.id === id) ? { ...rule, ...fields } : rule);
    setRules(newRules1);

    // TODO: add a "pending" field to the row, so we can see that the update is in progress

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

    // console.log("update", id, newRuleString);
    // update the state
    const newRules = rules.map((rule) => (rule.id === id) ? updatedRule : rule);
    setRules(newRules);

    // actually we should refresh everything to get the new match counts
    await fetchData();
    await fetchUnmatchedUrls();
  }

  function moveDelta(delta: number) {
    return async (id: number) => {
      // construct the url
      const url = `${apiBase}/filter_rules/${id}/`;
      // call the api
      const old_position = rules.find((rule) => rule.id === id)?.position;
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
      await fetchData();
    }
  }

  async function showDetails(id: number) {
    console.log("show details", id);
    setSelectedRuleDetails({});
    // fetch the details
    const url = `${apiBase}/filter_rules/${id}/matches`;
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);
    setSelectedRuleDetails(data);
  }

  useEffect(() => {
    console.log("rowSelection changed", rowSelection);
    const selectedRowId = Object.keys(rowSelection)[0];
    // get the row object (rule)
    const selectedRow = rules.find((rule) => rule.id === Number(selectedRowId));
    if (selectedRow) {
      showDetails(Number(selectedRowId));
    }
  }, [rowSelection, rules]);

  const selectedFilterRule = useMemo(() => {
    const selectedRowId = Object.keys(rowSelection)[0];
    if (selectedRowId) {
      return rules.find((rule) => rule.id === Number(selectedRowId));
    }
  }, [rowSelection, rules]);

  let detailUrls: string[];
  // selectedRuleDetails['new_matches'];
  if (selectedRuleDetails['new_matches'] !== undefined) {
    detailUrls = selectedRuleDetails['new_matches'];
  } else {
    detailUrls = [];
  }

  // iterate over all rules and pick the one with the last id
  let lastId = 0;
  for (let i = 0; i < rules.length; i++) {
    if (rules[i].id > lastId) {
      lastId = rules[i].id;
    }
  }


  const rows = rules;
  const columns: MRT_ColumnDef<Rule>[] = [
    {
      accessorKey: 'rule',
      header: 'URL Pattern',
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
            // const row = {...table.getState().creatingRow?.original || {}, ...data};
            // console.log("Combined row", row);
            //table.setCreatingRow(createRow(table, row));
            // table.setCreatingRow(null);
            // const r = table.getRow(""+row.id);
            // console.log("New row object", r);
            // table.setEditingRow(r);
            // console.log("Row is:", row);
            // //console.log("Attempting to set editing row to:", row);
            // const newRow = table.getRow(String(data.id));

            // table.setEditingRow(newRow);
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
          setRules(rules.filter((rule) => rule.id !== id));
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
    displayColumnDefOptions: {
      'mrt-row-drag': {
        header: 'Pos.',
        size: 10
      },
      'mrt-row-actions': {
        header: 'Actions',
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
    }
  });

  const sidebarOutlet = document.getElementById("sidebar-outlet");

  return (
    <div className="main-content">
      <p>{filterSet?.crawl_job.crawled_url_count} pages total, {filterSet?.remaining_urls} not handled yet</p>
      <h3>Rules</h3>

      <MaterialReactTable table={table} />

      <Stack direction="row" spacing={2} sx={{ mt: 2, mb: 2 }}>
        <Button variant="outlined" sx={{ textTransform: 'none' }}>Regel hinzufügen</Button>
        <Button variant="contained" style={{ textTransform: 'none', marginLeft: 'auto' }}>Start content crawl</Button>
      </Stack>

      {sidebarOutlet && createPortal(
        <FilterSetPageSidebar
          selectedFilterRule={selectedFilterRule}
          detailUrls={selectedFilterRule ? detailUrls : unmatchedUrls?.unmatched_urls || []} />,
        sidebarOutlet
      )}
    </div>
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
