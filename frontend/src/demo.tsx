// add the beginning of your app entry
import 'vite/modulepreload-polyfill'

import React from 'react'
import ReactDOM from 'react-dom/client'
import { Timeline } from './Timeline.tsx'
import './index.css'

document.writeln("WOLLOLO");


const root = document.getElementById('timeline')!;
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
const steps = [
  { number: 1, text: 'Start tree crawl', link: '/crawls/add' },
  { number: 2, text: 'Build filter', link: props.step2Link },
  { number: 3, text: 'Start content crawl' },
];

ReactDOM.createRoot(root).render(
  <React.StrictMode>
    <Timeline steps={steps} {...props} />
  </React.StrictMode>,
)
