import { useState, useEffect } from "react";
import RuleTable from "./RuleTable";
import { FilterSet, Rule, UnmatchedResponse } from "./schema";
import { useMemo } from 'react';
import { Checkbox, Input, Paper, Switch, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, ToggleButton } from "@mui/material";

import {
  getMRT_RowSelectionHandler,
  MaterialReactTable,
  MRT_RowSelectionState,
  useMaterialReactTable,
  type MRT_ColumnDef,
} from 'material-react-table';
import { createPortal } from "react-dom";

export default function FilterSetPage(props: { filterSetId: number, csrfToken: string }) {
  const [filterSet, setFilterSet] = useState<FilterSet | null>(null);
  const [rules, setRules] = useState<Rule[]>([]);
  const [detailsVisible, setDetailsVisible] = useState(false);
  // type is a json dict
  const [selectedRuleDetails, setSelectedRuleDetails] = useState({});
  const [unmatchedUrls, setUnmatchedUrls] = useState<UnmatchedResponse | null>(null);
    const [rowSelection, setRowSelection] = useState<MRT_RowSelectionState>({}); //ts type available

  const apiBase = "http://localhost:8000/api";
  const filterSetId = props.filterSetId;
  // console.log("filterSetId", filterSetId);

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


    //setRules(newRules);
  }

  async function updateFields(id: number, fields: { rule?: string, include?: boolean, page_type?: string}) {
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
    setDetailsVisible(true);
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
    // const selectedRow = rules.find((rule) => rule.id === Number(selectedRowId));
    if (selectedRowId) {
      showDetails(Number(selectedRowId));
    } else {
      setDetailsVisible(false);
    }
  }, [rowSelection]);

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
      muiEditTextFieldProps: ({ row }) => ({
        variant: "standard",
        fullWidth: true,
        slotProps: {
          input: { sx: { fontSize: 'inherit', m: -0, height: 22, marginTop: "2px", marginBottom: "-2px" } }
        },
        onBlur: (event) => {
          // table.setEditingCell(null) is called automatically onBlur internally
          updateFields(row.original.id, { rule: event.target.value });
        },
        // Make double click work properly: Don't select the whole text, but only the word under the cursor
        onDoubleClick: (event) => event.stopPropagation()
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
    // enableDensityToggle: false,
    enableFullScreenToggle: false,
    enableColumnActions: false,
    enableColumnFilters: false,
    enableSorting: false,
    enableHiding: false,
    enableTopToolbar: false,
    enableRowOrdering: true,
    enablePagination: false,
    enableEditing: true,
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
    },
    onRowSelectionChange: setRowSelection,
    state: { rowSelection },
    getRowId: (originalRow) => String(originalRow.id),
    // onRowSelectionChange: (rowSelection) => {
    //   console.log("rowSelection", rowSelection);
    //   const selectedRows = table.getSelectedRowModel().rows; //or read entire rows
    //   console.log("selectedRows", selectedRows);
    // },

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
    muiTableBodyCellProps: ({ cell, column, table }) => ({
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
    }),

  });

  const sidebarOutlet = document.getElementById("sidebar-outlet");

  return (
    <div className="main-content">
      <p>{filterSet?.crawl_job.crawled_url_count} pages total, {filterSet?.remaining_urls} not handled yet</p>
      <h3>Rules</h3>

      <MaterialReactTable table={table} />

      <RuleTable rules={rules}
        onDelete={deleteRow}
        onAdd={addRowAfter}
        onUpdateFields={(id, fields) => { updateFields(id, fields); }}
        onMoveUp={moveDelta(-1)}
        onMoveDown={moveDelta(1)}
        onShowDetails={showDetails}
      />

      <div style={{ display: 'flex', alignItems: 'center' }}>
        <button className="mybutton" onClick={() => addRowAfter(lastId)}>Add rule</button>
        <button className="mybutton mybutton-fancy"><s>Suggest rules</s></button>
        <div style={{ flex: 1 }}></div>
        <form action={`/filters/${filterSetId}/crawl/`} method="POST">
          <input type="hidden" name="csrfmiddlewaretoken" value={props.csrfToken} />
          <button className="mybutton">Start content crawl!</button>
        </form>
      </div>

      {/* {(detailsVisible && 
      <MatchesDialog onClose={() => setDetailsVisible(false)}
        detailUrls={detailUrls}/>)} */}

      {sidebarOutlet && createPortal(
        <div>
          <div style={{position: 'sticky'}}>
          <h3>Details</h3>

          <p>Ausgewählter Filter:</p>
          <p>Regel: <code>{selectedFilterRule?.rule}</code></p>
          <p>Treffer: <code>{selectedFilterRule?.count}</code></p>
          <p>Davon nicht durch vorherige Regeln erfasst: <code>{selectedFilterRule?.cumulative_count}</code></p>
          </div>

          <TableContainer component={Paper} >
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
        </div>
        ,
        sidebarOutlet
      )}

      <h3>Unmatched URLs</h3>
      {(unmatchedUrls &&
      <table className="table">
        <thead>
          <tr>
            <th>URL</th>
          </tr>
        </thead>
        <tbody>
          {unmatchedUrls.unmatched_urls.map((url) =>
          <tr key={url}>
            <td>{url}</td>
          </tr>)}
          {!unmatchedUrls.is_complete && <tr>
            <td><i>+ {unmatchedUrls.total_count - unmatchedUrls.unmatched_urls.length} URLs remaining</i></td>
          </tr>}
        </tbody>
      </table>
      )}
      </div>
  );
}