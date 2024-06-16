import { useEffect, useState } from 'react';
import './App.css';
import RuleTable from './RuleTable';
import { FilterSet, Rule } from './schema';


function App() {
  const [filterSet, setFilterSet] = useState<FilterSet | null>(null);
  const [rules, setRules] = useState<Rule[]>([]);
  // fetch data from http://127.0.0.1:8000/filter_sets/1/

  async function fetchData() {
    const url = "http://127.0.0.1:8000/filter_sets/1/";
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);
    setFilterSet(data);
    setRules(data.rules);
  }
  useEffect(() => {
    fetchData();
  }, []);


  async function deleteRow(id: number) {
    console.log("delete", id);

    const response = await fetch(`http://127.0.0.1:8000/filter_rules/${id}/`, {
      method: 'DELETE',
    });
    const data = await response.json();
    console.log(data);

    setRules(rules.filter((rule) => rule.id !== id));
  }

  async function addRowAfter(id: number) {
    console.log("add after", id);
    const newRule = {
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

  async function updateRow(id: number, newRuleString: string) {
    // call the api
    const url = `http://127.0.0.1:8000/filter_rules/${id}/`;
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ rule: newRuleString }),
    });
    const updatedRule = await response.json();
    console.log(updatedRule);

    console.log("update", id, newRuleString);
    // update the state
    const newRules = rules.map((rule) => (rule.id === id) ? updatedRule : rule);
    setRules(newRules);
  }

  function moveDelta(delta: number) {
    return async (id: number) => {
      // construct the url
      const url = `http://127.0.0.1:8000/filter_rules/${id}/`;
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
        },
        body: JSON.stringify({ position: old_position + delta }),
      });
      const updatedRule = await response.json();
      console.log(updatedRule);
      await fetchData();
    }
  }

  return (
    <div className="page">
      <h1>Generic Crawler</h1>
      <p>Filter #{filterSet?.id} '{filterSet?.name}' from {filterSet?.created_at}</p>
      <p>Crawl #{filterSet?.crawl_job.id} from {filterSet?.crawl_job.created_at}</p>
      <p>Start URL: {filterSet?.crawl_job.start_url}</p>
      <p>{filterSet?.crawl_job.url_count} pages total, XX not handled yet</p>
      <h3>Rules</h3>
      <RuleTable rules={rules}
        onDelete={deleteRow}
        onAdd={addRowAfter}
        onUpdate={(id, newRule) => { updateRow(id, newRule); console.log("onChange", id, newRule); }}
        onMoveUp={moveDelta(-1)}
        onMoveDown={moveDelta(1)}
      />

      <div>
        <button className="mybutton mybutton-fancy">Suggest rules</button>
      </div>
    </div>
  );
}

export default App
