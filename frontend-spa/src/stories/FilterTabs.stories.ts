import type { Meta, StoryObj } from '@storybook/react-vite';
import { fn } from 'storybook/test';
import FilterTabs from '../FilterTabs';
import { TabInfo } from '../FilterTabs';
import ErrorIcon from '../assets/icons/error.svg?react';
import EditIcon from '../assets/icons/mode_edit.svg?react';
import PendingIcon from '../assets/icons/pending.svg?react';
import StopIcon from '../assets/icons/stop.svg?react';

const meta: Meta<typeof FilterTabs> = {
  title: 'Components/FilterTabs',
  component: FilterTabs,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    style: {
      control: 'select',
      options: ['filter', 'sidebar'],
    },
    tabsClickable: {
      control: 'select',
      options: ['all', 'complete'],
    },
    selectedTab: {
      control: { type: 'number', min: 0, max: 7 },
    },
  },
  args: {
    onTabClick: fn(),
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

// Example tabs based on DashboardPage.tsx usage
const dashboardTabs: TabInfo[] = [
  { tag: "all", label: "Alle" },
  { tag: "draft", label: "Entwurf", icon: EditIcon },
  { tag: "pending", label: "Gecrawlt", icon: PendingIcon },
  { tag: "stopped", label: "Gestoppt", icon: StopIcon },
  { tag: "error", label: "Fehler", icon: ErrorIcon },
  { tag: "published", label: "Im Prüfbuffet", icon: ErrorIcon },
];

const dashboardTabsStringIcons: TabInfo[] = [
  { tag: "all", label: "Alle" },
  { tag: "draft", label: "Entwurf", icon: "edit" },
  { tag: "pending", label: "Gecrawlt", icon: "pending" },
  { tag: "stopped", label: "Gestoppt", icon: "stop" },
  { tag: "error", label: "Fehler", icon: "error" },
  { tag: "published", label: "Im Prüfbuffet", icon: "robot" },
];

const simpleTabs: TabInfo[] = [
  { label: "Tab 1" },
  { label: "Tab 2" },
  { label: "Tab 3" },
  { label: "Tab 4" },
];

const manyTabs: TabInfo[] = [
  { label: "Übersicht" },
  { label: "Benutzer", icon: EditIcon },
  { label: "Einstellungen", icon: PendingIcon },
  { label: "Berichte", icon: StopIcon },
  { label: "Analytics", icon: ErrorIcon },
  { label: "Export", icon: EditIcon },
  { label: "Import", icon: PendingIcon },
  { label: "Backup", icon: StopIcon },
];

export const Default: Story = {
  args: {
    tabs: dashboardTabs,
    selectedTab: 0,
    style: 'filter',
    tabsClickable: 'all',
  },
};

export const UsingStringAsIcons: Story = {
  args: {
    tabs: dashboardTabsStringIcons,
    selectedTab: 0,
    style: 'filter',
    tabsClickable: 'all',
  },
};

export const WithSelectedTab: Story = {
  args: {
    tabs: dashboardTabs,
    selectedTab: 2,
    style: 'filter',
    tabsClickable: 'all',
  },
};

export const SidebarStyle: Story = {
  args: {
    tabs: dashboardTabs,
    selectedTab: 1,
    style: 'sidebar',
    tabsClickable: 'all',
  },
};

export const OnlyCompletedClickable: Story = {
  args: {
    tabs: dashboardTabs,
    selectedTab: 3,
    style: 'sidebar',
    tabsClickable: 'complete',
  },
};

export const SimpleTabs: Story = {
  args: {
    tabs: simpleTabs,
    selectedTab: 1,
    style: 'filter',
    tabsClickable: 'all',
  },
};

export const ManyTabs: Story = {
  args: {
    tabs: manyTabs,
    selectedTab: 4,
    style: 'filter',
    tabsClickable: 'all',
  },
};

export const NoSelection: Story = {
  args: {
    tabs: dashboardTabs,
    selectedTab: undefined,
    style: 'filter',
    tabsClickable: 'all',
  },
};