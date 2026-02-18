import Delete from '@mui/icons-material/Delete';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Switch from '@mui/material/Switch';
import { Stack } from "@mui/system";
import {
    getMRT_RowSelectionHandler,
    MaterialReactTable,
    MRT_RowSelectionState,
    useMaterialReactTable,
    type MRT_ColumnDef
} from 'material-react-table';
import { EvaluateFiltersResult } from './apitypes';
import { Rule } from "./schema";


export default function FilterSetTable(props: {
  evaluationResult: EvaluateFiltersResult,
  rowSelection: MRT_RowSelectionState,
  setRowSelection: React.Dispatch<React.SetStateAction<MRT_RowSelectionState>>,
  addRowWithDataAfter: (id: number, ruleData: { rule: string }) => Promise<Rule>,
  updateFields: (id: number, fields: { rule?: string, include?: boolean, page_type?: string }) => Promise<void>,
  doMoveRule: (draggedId: number, hoveredPosition: number) => Promise<void>,
  doDeleteRule: (id: number) => void,
  evaluateFilters: () => Promise<void>,
  onStartContentCrawl: () => void,
}) {

  const { evaluationResult, rowSelection, setRowSelection, addRowWithDataAfter, updateFields, doMoveRule, doDeleteRule, evaluateFilters, onStartContentCrawl } = props;

  const lastId = Math.max(...evaluationResult.rules.map(r => r.id), 0);
  const lastPosition = Math.max(...evaluationResult.rules.map(r => r.position), 0);

  const sortedRows = [...evaluationResult.rules].sort((a, b) => a.position - b.position)
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
      muiEditTextFieldProps: ({ row, table }) => ({
        variant: "standard",
        fullWidth: true,
        slotProps: {
          input: { sx: { fontSize: 'inherit', m: -0, height: 22, marginTop: "2px", marginBottom: "-2px" } }
        },
        onKeyDown: async (event) => {
          if (event.key === 'Enter') {
            event.preventDefault();
            if (table.getState().creatingRow) {
              await addRowWithDataAfter(lastId, { rule: (event.target as HTMLInputElement).value });
              table.setCreatingRow(null);
            } else {
              (event.target as HTMLInputElement).blur();
            }
          }
        },
        onBlur: async (event) => {
          if (table.getState().creatingRow) {
            // Don't save on blur during row creation — onCreatingRowSave handles it
            return;
          }
          updateFields(row.original.id, { rule: event.target.value });
        },
        // Make double click work properly: Don't select the whole text, but only the word under the cursor
        onDoubleClick: (event) => event.stopPropagation(),
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

        await doMoveRule(draggedId, hoveredPosition);
      },
    }),
    enablePagination: false,
    enableEditing: true,
    enableRowActions: true,
    positionActionsColumn: 'last',
    renderRowActions: ({ row }) => (
      (row.original.id !== -1) && (
        <IconButton onClick={() => console.info('Delete')}>
          <Delete onClick={() => doDeleteRule(row.original.id)} />
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
      // single click to select row
      onClick: (event) => {
        if (row.id === 'mrt-row-create') return;
        getMRT_RowSelectionHandler({ row, staticRowIndex, table })(event);
      },
    }),
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
        paddingLeft: column.id === 'mrt-row-drag' ? 2 : column.id === 'mrt-row-actions' ? 0 : 1,
        paddingRight: column.id === 'mrt-row-drag' ? 0 : column.id === 'mrt-row-actions' ? 0 : 1,
        boxSizing: 'border-box',
      },
    }),
    muiTableBodyCellProps: ({ column }) => ({
      sx: {
        paddingLeft: column.id === 'mrt-row-drag' ? 2 : column.id === 'mrt-row-actions' ? 0 : 1,
        paddingRight: column.id === 'mrt-row-drag' ? 0 : column.id === 'mrt-row-actions' ? 0 : 1,
        boxSizing: 'border-box',
      },
    }),
    positionToolbarAlertBanner: 'none',
    createDisplayMode: 'row',
    positionCreatingRow: rows.length-1,
    onCreatingRowSave: async ({ table, values }) => {
      await addRowWithDataAfter(lastId, values);
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
        flexShrink: 1,
      },
    },
  });


  return <> <MaterialReactTable table={table} />

    <Stack direction="row" spacing={2} sx={{ mt: 1 }}>
      <Button variant="outlined" sx={{ textTransform: 'none' }} onClick={() => table.setCreatingRow(true)}>Regel hinzufügen</Button>
      <Button variant='outlined' sx={{ textTransform: 'none' }} onClick={evaluateFilters}>Filter auswerten</Button>
      <Button variant="contained" style={{ textTransform: 'none', marginLeft: 'auto' }} onClick={onStartContentCrawl}>Start content crawl</Button>
    </Stack>
  </>;
}
