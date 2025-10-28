// add the beginning of your app entry
import 'vite/modulepreload-polyfill'

import React from 'react'
import ReactDOM from 'react-dom/client'
// import { Timeline } from './Timeline.tsx'
import './index.css'
import { Button, MetadataInheritancePage, FilterTabs, TabInfo } from 'wlo-components';
import 'wlo-components/styles'; // CSS-Datei importieren
import { MemoryRouter } from 'react-router-dom';

document.writeln("WOLLOLO");


const root = document.getElementById('spa_root')!;
console.log("root:", root);
// convert all the "data-" attributes to a javascript object that we
// can pass as props to the component
const camelize = s => s.replace(/-./g, x=>x[1].toUpperCase())
const props = Object.fromEntries(
  Array.from(root.attributes)
    .filter(attr => attr.name.startsWith('data-'))
    .map(attr => [camelize(attr.name.slice(5)), attr.value])
)

console.log("props:", props);
// const steps = [
//   { number: 1, text: 'Start tree crawl', link: '/crawls/add' },
//   { number: 2, text: 'Build filter', link: props.step2Link },
//   { number: 3, text: 'Start content crawl' },
// ];

const dashboardTabs: TabInfo[] = [
  { tag: "all", label: "Alle" },
  { tag: "draft", label: "Entwurf", icon: 'edit' },
  { tag: "pending", label: "Gecrawlt", icon: 'pending' },
  { tag: "stopped", label: "Gestoppt", icon: 'stop' },
  { tag: "error", label: "Fehler", icon: 'error' },
  { tag: "published", label: "Im Prüfbuffet", icon: 'error' },
];

function App() {
  const [selectedTab, setSelectedTab] = React.useState<number>(0);
  return (
    <div>
    <MemoryRouter initialEntries={['/']}>
      <FilterTabs tabs={dashboardTabs} selectedTab={selectedTab} onTabClick={setSelectedTab} />
      <MetadataInheritancePage />
      <Button default={true}>Click Me</Button>
    </MemoryRouter>
    </div>
  );
}

ReactDOM.createRoot(root).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
