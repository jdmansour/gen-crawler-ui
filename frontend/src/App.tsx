import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import RuleTable from './RuleTable'


const initialRules = [
  {
    "id": 1,
    "url_pattern": "https://example.com/blog/...",
    "matches": 344,
    "include": "Yes",
    "type": "Article"
  },
  {
    "id": 2,
    "url_pattern": "https://example.com/videos/...",
    "matches": 123,
    "include": "Yes",
    "type": "(Pointer to) Video"
  },
  {
    "id": 3,
    "url_pattern": "https://example.com/videos/about",
    "matches": 1,
    "include": "No",
    "type": "-"
  }
]


const filterSetExample = {
      "id": 2,
      "crawl_job": {
          "id": 6,
          "start_url": "https://weltderphysik.de",
          "follow_links": true,
          "created_at": "2024-06-12T11:41:37.056465Z",
          "updated_at": "2024-06-12T11:41:37.058759Z"
      },
      "name": "Test",
      "created_at": "2024-06-14T08:29:50.221698Z",
      "updated_at": "2024-06-14T08:29:50.221712Z",
      "url": "http://127.0.0.1:8000/filter_sets/2/",
      "rules": [
          {
              "id": 3,
              "rule": "Blah",
              "include": false,
              "created_at": "2024-06-14T09:49:18.166863Z",
              "updated_at": "2024-06-14T09:49:18.166927Z",
              "page_type": "Blub",
              "count": 100
          },
          {
              "id": 4,
              "rule": "Blah",
              "include": false,
              "created_at": "2024-06-14T09:55:31.738095Z",
              "updated_at": "2024-06-14T09:55:31.738136Z",
              "page_type": "Blub",
              "count": 100
          },
          {
              "id": 5,
              "rule": "https://example.com/videos/...",
              "include": true,
              "created_at": "2024-06-14T09:55:57.020011Z",
              "updated_at": "2024-06-14T09:55:57.020128Z",
              "page_type": "New row",
              "count": 123
          }
      ]
  };

type CrawlJob = {
  id: number,
  start_url: string,
  follow_links: boolean,
  created_at: string,
  updated_at: string,
}

type Rule = {
  id: number,
  rule: string,
  count: number,
  include: boolean,
  page_type: string,
}

type FilterSet = {
  id: number,
  crawl_job: CrawlJob,
  name: string,
  created_at: string,
  updated_at: string,
  url: string,
  rules: Rule[],
}




function App() {
  let [filterSet, setFilterSet] = useState<FilterSet|null>(null);
  let [rules, setRules] = useState(initialRules);
  // fetch data from http://127.0.0.1:8000/filter_sets/1/
  useEffect(() => {
    async function fetchData() {
      const url = "http://127.0.0.1:8000/filter_sets/1/";
      const response = await fetch(url);
      const data = await response.json();
      console.log(data);
      setFilterSet(data);
      setRules(data.rules);
    }
    fetchData();
  }, []);


  async function deleteRow(id: number) {
    console.log("delete", id);
    
    const response = await fetch(`http://127.0.0.1:8000/filter_rules/${id}/`, {
      method: 'DELETE',
    });
    const data = await response.json();
    console.log(data);

    //rules = rules.filter((rule) => rule.id !== id);
    setRules(rules.filter((rule) => rule.id !== id));
  }

  // function addRowAfter(id: number) {
  //   console.log("add after", id);
  //   let newRule = {
  //     "id": 4,
  //     "url_pattern": "https://example.com/videos/...",
  //     "matches": 123,
  //     "include": "Yes",
  //     "type": "New row"
  //   }
  //   //setRules([...rules, newRule]);
  //   // insert after rule with the id
  //   let newRules = [];
  //   for (let rule of rules) {
  //     newRules.push(rule);
  //     if (rule.id === id) {
  //       newRules.push(newRule);
  //     }
  //   }
  //   setRules(newRules);
  // }

  async function addRowAfter(id: number) {
    console.log("add after", id);
    let newRule = {
      // TODO: how to make it so we can use an ID and not a URL?
      "filter_set": "http://127.0.0.1:8000/filter_sets/1/",
      //"filter_set": "1",
      "rule": "https://www.weltderphysik.de/wir",
      "count": 123,
      "include": true,
      "page_type": "New row"
    }
    //setRules([...rules, newRule]);
    // insert after rule with the id
    const post_url = "http://127.0.0.1:8000/filter_rules/";
    const response = await fetch(post_url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newRule),
    });
    const data = await response.json();
    console.log(data);
    // TODO: add ordering
    setRules([...rules, data]);


    //setRules(newRules);
  }

  return (
    <div className="page">
      <h1>Generic Crawler</h1>
      <p>Crawl #C4 from 2024-06-13</p>
      <p>Filter #{filterSet?.id} '{filterSet?.name}' from 2024-06-14</p>
      <p>Start URL: {filterSet?.crawl_job.start_url}</p>
      <p>604 pages total, 5 not handled yet</p>
      <h3>Rules</h3>
      <RuleTable rules={rules} onDelete={deleteRow} onAdd={addRowAfter} />

      <div>
        <button className="mybutton mybutton-fancy">Suggest rules</button>
      </div>
    </div>
  );


  // const [count, setCount] = useState(0)

  // return (
  //   <>
  //     <div>
  //       <a href="https://vitejs.dev" target="_blank">
  //         <img src={viteLogo} className="logo" alt="Vite logo" />
  //       </a>
  //       <a href="https://react.dev" target="_blank">
  //         <img src={reactLogo} className="logo react" alt="React logo" />
  //       </a>
  //     </div>
  //     <h1>Vite + Reacts</h1>
  //     <div className="card">
  //       <button onClick={() => setCount((count) => count + 1)}>
  //         count is {count}
  //       </button>
  //       <p>
  //         Edit <code>src/App.tsx</code> and save to test HMR
  //       </p>
  //     </div>
  //     <p className="read-the-docs">
  //       Click on the Vite and React logos to learn more
  //     </p>
  //   </>
  // )
}

export default App
