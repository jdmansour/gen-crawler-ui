import * as React from 'react';
import Box from '@mui/material/Box';
import Checkbox from '@mui/material/Checkbox';
import CheckBoxOutlineBlank from '@mui/icons-material/CheckBoxOutlineBlank';
import { RichTreeView } from '@mui/x-tree-view/RichTreeView';
import {
  TreeItem,
  TreeItemProps,
  TreeItemSlotProps,
} from '@mui/x-tree-view/TreeItem';

type TreeItemType = {
  id: string;
  label: string;
  disabled?: boolean;
  editable?: boolean;
  children?: TreeItemType[];
};

const SITEMAP_ITEMS: TreeItemType[] = [
  {
    id: 'grundlagen',
    label: 'Grundlagen',
    children: [
      {
        id: 'grundlagen-funktionen',
        label: 'Funktionen',
        children: [
          { id: 'grundlagen-funktionen-konzept', label: 'Das Funktionskonzept' },
          { id: 'grundlagen-funktionen-klassen', label: 'Funktionenklassen' },
        ],
      },
      {
        id: 'grundlagen-folgen',
        label: 'Folgen',
        children: [
          { id: 'grundlagen-folgen-konzept', label: 'Das Folgenkonzept' },
          { id: 'grundlagen-folgen-eigenschaften', label: 'Eigenschaften von Folgen' },
        ],
      },
      {
        id: 'grundlagen-grenzwerte',
        label: 'Grenzwerte',
        children: [
          { id: 'grundlagen-grenzwerte-folgen', label: 'Grenzverhalten von Folgen' },
          { id: 'grundlagen-grenzwerte-praezisierung', label: 'Präzisierung des Grenzwertbegriffs' },
          { id: 'grundlagen-grenzwerte-funktionen', label: 'Grenzwerte bei Funktionen' },
          { id: 'grundlagen-grenzwerte-stetigkeit', label: 'Stetigkeit von Funktionen' },
        ],
      },
    ],
  },
  {
    id: 'differentialrechnung',
    label: 'Differentialrechnung',
    children: [
      {
        id: 'diff-ableitung-stelle',
        label: 'Ableitung an einer Stelle',
        children: [
          { id: 'diff-ableitung-stelle-bestand', label: 'Entwicklung eines Bestandes' },
          { id: 'diff-ableitung-stelle-mittlere', label: 'Mittlere Änderungsrate' },
          { id: 'diff-ableitung-stelle-lokal', label: 'Ableitung als lokale Änderungsrate' },
          { id: 'diff-ableitung-stelle-diffbar', label: 'Differenzierbarkeit' },
        ],
      },
      {
        id: 'diff-ableitung-funktionen',
        label: 'Ableitung von Funktionen',
        children: [
          { id: 'diff-ableitung-funktionen-ableitungsfunktion', label: 'Ableitungsfunktion' },
          { id: 'diff-ableitung-funktionen-grafisch', label: 'Grafisches Ableiten' },
          { id: 'diff-ableitung-funktionen-regeln', label: 'Elementare Ableitungsregeln' },
          { id: 'diff-ableitung-funktionen-hoehere', label: 'Höhere Ableitungen' },
          { id: 'diff-ableitung-funktionen-geometrie', label: 'Ableitungsgeometrie' },
        ],
      },
      {
        id: 'diff-funktionsuntersuchungen',
        label: 'Funktionsuntersuchungen',
        children: [
          { id: 'diff-funktionsuntersuchungen-eigenschaften', label: 'Eigenschaften von Funktionen' },
          { id: 'diff-funktionsuntersuchungen-nullstellen', label: 'Nullstellen von Funktionen' },
          { id: 'diff-funktionsuntersuchungen-monotonie', label: 'Monotonie und lokale Extrema' },
          { id: 'diff-funktionsuntersuchungen-extrema', label: 'Bestimmung lokaler Extrema' },
          { id: 'diff-funktionsuntersuchungen-wendepunkte', label: 'Krümmung und Wendepunkte' },
        ],
      },
      {
        id: 'diff-anwendungen',
        label: 'Anwendungen',
        children: [
          { id: 'diff-anwendungen-optimierung', label: 'Optimierungsprobleme' },
          { id: 'diff-anwendungen-bestimmung', label: 'Funktionsbestimmung' },
          { id: 'diff-anwendungen-parameter', label: 'Funktionen mit Parametern' },
        ],
      },
      {
        id: 'diff-exponential',
        label: 'Exponentialfunktionen',
        children: [
          { id: 'diff-exponential-prozesse', label: 'Exponentielle Prozesse' },
          { id: 'diff-exponential-ableitung', label: 'Ableitung von Exponentialfunktionen' },
          { id: 'diff-exponential-efunktion', label: 'e-Funktion und ln-Funktion' },
          { id: 'diff-exponential-parameter', label: 'e-Funktion mit Parametern' },
          { id: 'diff-exponential-halbwertszeit', label: 'Verdopplungs- und Halbwertszeit' },
        ],
      },
    ],
  },
  {
    id: 'integralrechnung',
    label: 'Integralrechnung',
  },
  {
    id: 'analytische-geometrie',
    label: 'Analytische Geometrie',
  },
];


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

const ITEMS_BY_DEPTH = getItemsByDepth(SITEMAP_ITEMS);

const DepthContext = React.createContext(0);

const CHECKBOX_COLORS = ['primary', 'secondary', 'success', 'warning'] as const;

const CustomTreeItem = React.forwardRef(function CustomTreeItem(
  props: TreeItemProps,
  ref: React.Ref<HTMLLIElement>
) {
  const depth = React.useContext(DepthContext);
  const color = CHECKBOX_COLORS[depth % CHECKBOX_COLORS.length];

  return (
    <DepthContext.Provider value={depth + 1}>
      <TreeItem
        {...props}
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

export default function CheckboxSelection() {
  const [selectedItems, setSelectedItems] = React.useState<string[]>([]);

  const handleDepthToggle = (depth: number) => {
    const depthIds = ITEMS_BY_DEPTH.get(depth) ?? [];
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
          defaultExpandedItems={['differentialrechnung', 'integralrechnung']}
          checkboxSelection
          multiSelect={true}
          selectedItems={selectedItems}
          onSelectedItemsChange={(_event, ids) => setSelectedItems(ids)}
          items={SITEMAP_ITEMS}
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
      <Box sx={{ borderTop: 1, borderColor: 'divider', display: 'flex', pl: '30px' }}>
        {Array.from(ITEMS_BY_DEPTH.keys()).sort().map(depth => {
          const depthIds = ITEMS_BY_DEPTH.get(depth)!;
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
      </Box>
    </Box>
  );
}
