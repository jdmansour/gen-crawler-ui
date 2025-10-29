// Exportiere nur die essentiellen Komponenten
export { default as MetadataInheritancePage } from './MetadataInheritancePage';
export { default as Button } from './Button';
export { default as Breadcrumbs } from './Breadcrumbs';
export { CustomIcon } from './CustomIcon';
export { default as FilterTabs } from './FilterTabs';
export { default as InputWithButton } from './InputWithButton';
export { default as ListView } from './ListView';
export { default as Sheet } from './Sheet';
export { default as GenCrawlerSidebar } from './GenCrawlerSidebar';
export { default as DashboardPage } from './DashboardPage';
export { default as FilterCrawlsPage } from './FilterCrawlsPage';
export { default as SelectSourcePage } from './SelectSourcePage';
export { default as SiteLayout } from './SiteLayout';
export { ShowSidebarButton } from './SiteLayout';


// Types
export type { TabInfo, TabsStyle } from './FilterTabs';
export type { Breadcrumb } from './Breadcrumbs';

// CSS-Module Styles (werden automatisch von Vite verarbeitet)
import './FilterTabs.module.css';