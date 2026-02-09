import * as React from 'react';
import Box from '@mui/material/Box';
import Checkbox from '@mui/material/Checkbox';
import CheckBoxOutlineBlank from '@mui/icons-material/CheckBoxOutlineBlank';
import Tooltip from '@mui/material/Tooltip';
import { RichTreeView } from '@mui/x-tree-view/RichTreeView';
import { useTreeItemModel } from '@mui/x-tree-view/hooks';
import {
  TreeItem,
  TreeItemProps,
  TreeItemSlotProps,
} from '@mui/x-tree-view/TreeItem';
import { Typography } from '@mui/material';

export type TreeItemType = {
  id: string;
  label: string;
  url?: string;
  disabled?: boolean;
  editable?: boolean;
  children?: TreeItemType[];
};

interface SitemapTreeProps {
  items: TreeItemType[];
}


function getExpandableIds(items: TreeItemType[]): string[] {
  const ids: string[] = [];
  function walk(items: TreeItemType[]) {
    for (const item of items) {
      if (item.children?.length) {
        ids.push(item.id);
        walk(item.children);
      }
    }
  }
  walk(items);
  return ids;
}

function getItemsByDepth(items: TreeItemType[]): Map<number, string[]> {
  const result = new Map<number, string[]>();
  function walk(items: TreeItemType[], depth: number) {
    for (const item of items) {
      if (!result.has(depth)) result.set(depth, []);
      result.get(depth)!.push(item.id);
      if (item.children) walk(item.children, depth + 1);
    }
  }
  walk(items, 0);
  return result;
}

const DepthContext = React.createContext(0);

const CHECKBOX_COLORS = ['primary', 'secondary', 'success', 'warning'] as const;

const CustomTreeItem = React.forwardRef(function CustomTreeItem(
  props: TreeItemProps,
  ref: React.Ref<HTMLLIElement>
) {
  const depth = React.useContext(DepthContext);
  const color = CHECKBOX_COLORS[depth % CHECKBOX_COLORS.length];
  const item = useTreeItemModel<TreeItemType>(props.itemId);

  const label = item?.url ? (
    <Tooltip title={item.url} placement="right" enterDelay={500}>
      <span>{props.label}</span>
    </Tooltip>
  ) : props.label;

  return (
    <DepthContext.Provider value={depth + 1}>
      <TreeItem
        {...props}
        label={label}
        ref={ref}
        slotProps={
          {
            checkbox: {
              size: 'small',
              color,
              icon: <CheckBoxOutlineBlank color={color} />,
            //   checkedIcon: <Favorite color={color} />,
              indeterminateIcon: <CheckBoxOutlineBlank color={color} />,
            },
          } as TreeItemSlotProps
        }
      />
    </DepthContext.Provider>
  );
});

export default function SitemapTree({ items }: SitemapTreeProps) {
  const [selectedItems, setSelectedItems] = React.useState<string[]>([]);
  const defaultExpandedItems = React.useMemo(() => getExpandableIds(items), [items]);
  const itemsByDepth = React.useMemo(() => getItemsByDepth(items), [items]);

  const handleDepthToggle = (depth: number) => {
    const depthIds = itemsByDepth.get(depth) ?? [];
    const allSelected = depthIds.every(id => selectedItems.includes(id));
    if (allSelected) {
      setSelectedItems(prev => prev.filter(id => !depthIds.includes(id)));
    } else {
      setSelectedItems(prev => [...new Set([...prev, ...depthIds])]);
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: 500, minWidth: 350 }}>
      <Box sx={{ flex: 1, overflow: 'auto' }}>
        <RichTreeView
          defaultExpandedItems={defaultExpandedItems}
          checkboxSelection
          multiSelect={true}
          selectedItems={selectedItems}
          onSelectedItemsChange={(_event, ids) => setSelectedItems(ids)}
          items={items}
          slots={{ item: CustomTreeItem }}
          itemChildrenIndentation={24}
          expansionTrigger="iconContainer"
          onItemClick={(event) => {
            const target = event.target as HTMLElement;
            if (target.closest('.MuiCheckbox-root, .MuiTreeItem-iconContainer')) return;
            const itemEl = target.closest('.MuiTreeItem-root');
            const checkbox = itemEl?.querySelector(
              ':scope > .MuiTreeItem-content .MuiCheckbox-root input'
            ) as HTMLElement | null;
            checkbox?.click();
            event.stopPropagation();
          }}
        />
      </Box>
      <Box sx={{ borderTop: 1, borderColor: 'divider', display: 'flex', pl: '30px'  }} alignItems="center">
        {Array.from(itemsByDepth.keys()).sort().map(depth => {
          const depthIds = itemsByDepth.get(depth)!;
          const selectedCount = depthIds.filter(id => selectedItems.includes(id)).length;
          const color = CHECKBOX_COLORS[depth % CHECKBOX_COLORS.length];
          return (
            <Checkbox
              key={depth}
              size="small"
              color={color}
              icon={<CheckBoxOutlineBlank color={color} />}
              checked={selectedCount === depthIds.length}
              indeterminate={selectedCount > 0 && selectedCount < depthIds.length}
              onChange={() => handleDepthToggle(depth)}
              sx={{ p: 0, width: 24, height: 38 }}
            />
          );
        })}
        { /* add label describing the checkboxes */}
        {/* <Box sx={{ ml: 1, color: 'text.secondary', fontSize: '0.875rem', fontFamily: 'Roboto, Helvetica, Arial, sans-serif' }}> */}
        <Typography variant="body2" color="text.secondary" sx={{ ml: 1, mt: "2px" }}>
          Alle Elemente einer Tiefe aus-/abwählen
        </Typography>
        {/* </Box> */}
      </Box>
    </Box>
  );
}
