import { Skeleton } from '@mui/material';
import { MRT_RowSelectionState } from 'material-react-table';
import { JSX, useCallback, useEffect, useMemo, useState } from "react";
import { createPortal } from "react-dom";
import { useOutletContext, useParams } from 'react-router';
import { EvaluateFiltersResult, RuleEvaluation } from './apitypes';
import FilterSetPageSidebar from './FilterSetPageSidebar';
import FilterSetTable from './FilterSetTable';
import { FilterSetPageContext } from './RootContext';
import { Rule } from "./schema";
import { useStep } from "./steps";

const apiBase = "http://localhost:8000/api";

export default function FilterSetPage(props: { csrfToken: string }) {
  // type is a json dict
  const [rowSelection, setRowSelection] = useState<MRT_RowSelectionState>({});
  const [evaluationResult, setEvaluationResult] = useState<EvaluateFiltersResult>({ id: 0, remaining_urls: 0, name: "", created_at: "", updated_at: "", rules: [] });
  const { crawlerList, crawlerListLoaded } = useOutletContext<FilterSetPageContext>();
  // const crawlJobId = 14;  // TODO: make dynamic
  const { crawlerId } = useParams();

  const crawler = crawlerList.find(c => c.id === Number(crawlerId));

  // // get crawler from crawlerList matching filterSetId
  // const crawler = crawlerList.find(c => c.filter_set_id === props.filterSetId);
  // pick the crawl job with the latest updated_at
  const crawlJob = crawler?.crawl_jobs.reduce((latest, job) => {
    return new Date(job.updated_at) > new Date(latest.updated_at) ? job : latest;
  }, crawler.crawl_jobs[0]);

  // todo: handle case where crawler or crawlJob is undefined
  const crawlJobId = crawlJob?.id;
  const filterSetId = crawler?.filter_set_id;
  // const filterSetId = props.filterSetId;
  console.log("FilterSetPage crawlerId", crawlerId, "crawlJobId", crawlJobId, "filterSetId", filterSetId);
  console.log("crawlerList.length", crawlerList.length);
  useStep('filters')

  const evaluateFilters = useCallback(async () => {
    if (crawlJobId === undefined) {
      console.warn("crawlJobId is undefined, cannot evaluate filters");
      return;
    }

    const url = apiBase + `/crawl_jobs/${crawlJobId}/evaluate_filters/`;
    // POST
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': props.csrfToken,
      },
      body: JSON.stringify({}),
    });
    if (!response.ok) {
      console.error("Failed to evaluate filters");
      return;
    }
    const data: EvaluateFiltersResult = await response.json();
    setEvaluationResult(data);
  }, [crawlJobId, props.csrfToken]);
  
  useEffect(() => {
    evaluateFilters();
  }, [evaluateFilters]);

  async function addRowWithDataAfter(id: number, ruleData: { rule: string }): Promise<Rule> {
    console.log("add after", id);
    const filterSetUrl = apiBase + `/filter_sets/${filterSetId}/`;
    console.log("filterSetUrl", filterSetUrl);
    const newRule = {
      // TODO: how to make it so we can use an ID and not a URL?
      "filter_set": filterSetUrl,
      //"filter_set": "1",
      "rule": ruleData.rule,
      "count": 666,
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
    //setRules([...rules, data]);
    setEvaluationResult({ ...evaluationResult, rules: [...evaluationResult.rules, data] });
    return data;
  }

  async function updateFields(id: number, fields: { rule?: string, include?: boolean, page_type?: string }) {
    // Update the fields in the row right away
    // TODO: add a "pending" field to the row, so we can see that the update is in progress
    const newRules1 = evaluationResult.rules.map((rule) => (rule.id === id) ? { ...rule, ...fields } : rule);
    setEvaluationResult({ ...evaluationResult, rules: newRules1 });

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

    // actually we should refresh everything to get the new match counts
    await evaluateFilters();
  }

  async function doMoveRule(draggedId: number, hoveredPosition: number) {
    const url = `${apiBase}/filter_rules/${draggedId}/`;
    // call PATCH and update position to the position of where it was dropped
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': props.csrfToken,
      },
      body: JSON.stringify({ position: hoveredPosition }),
    });
    const data = await response.json();
    console.log("Move response", data);

    // Update local state so we get immediate feedback
    // const newRules = moveRule(evaluationResult.rules, draggedId, hoveredPosition);
    // for (let i = 0; i < newRules.length; i++) {
    //   console.log("Moving rule", newRules[i].id, "from", evaluationResult.rules[i].position, "to", newRules[i].position);
    // }
    // setEvaluationResult({ ...evaluationResult, rules: newRules });
    setEvaluationResult(prev => ({ ...prev, rules: moveRule(prev.rules, draggedId, hoveredPosition) }));

    // re-evaluate filters to get updated counts
    await evaluateFilters();
  }

  async function doDeleteRule(id: number) {
    const response = await fetch(`${apiBase}/filter_rules/${id}/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': props.csrfToken,
      },
    });
    const data = await response.json();
    console.log("delete response: ", data);
    setEvaluationResult({ ...evaluationResult, rules: evaluationResult.rules.filter((rule) => rule.id !== id) });
  }

  const selectedFilterRule = useMemo(() => {
    const selectedRowId = Object.keys(rowSelection)[0];
    if (selectedRowId) {
      return evaluationResult.rules.find((rule) => rule.id === Number(selectedRowId));
    }
  }, [rowSelection, evaluationResult.rules]);
  
  const sidebarOutlet = document.getElementById("sidebar-outlet");

  let content: JSX.Element;
  if (!crawlerListLoaded) {
    content = <Skeleton variant="rounded" animation="wave" width={"100%"} height={200} />;
  } else if (filterSetId === undefined || filterSetId === null) {
    content = <div>Fehler: Kein filter_set gefunden</div>;
  } else if (crawlJobId === undefined || crawlJobId === null) {
    content = <div>Fehler: Kein crawl job gefunden</div>;
  } else {
    content = <FilterSetTable 
      evaluationResult={evaluationResult}
      rowSelection={rowSelection}
      setRowSelection={setRowSelection}
      addRowWithDataAfter={addRowWithDataAfter}
      updateFields={updateFields}
      doMoveRule={doMoveRule}
      doDeleteRule={doDeleteRule}
      evaluateFilters={evaluateFilters}
    />
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", flex: 1,
                        padding: "8px 24px 16px 24px", gap: "16px", flexShrink: 1, minHeight: 350}}>
      <h2 style={{ margin: "0px 0px" }}>Filterregeln</h2>

      <div><a href={`http://localhost:8000/admin/crawls/filterset/${filterSetId}/change/`}>Filter set {filterSetId}</a></div>
      <div><a href={`http://localhost:8000/admin/crawls/crawljob/${crawlJobId}/change/`}>Data from crawl job {crawlJobId}</a></div>
      <div>Crawler list loaded: {crawlerListLoaded ? "Yes" : "No"}</div>

      {content}

      {sidebarOutlet && createPortal(
        <FilterSetPageSidebar
          filterSetId={filterSetId || null}
          crawlJobId={crawlJobId || null}
          selectedFilterRule={selectedFilterRule} />,
        sidebarOutlet
      )}
    </div>
  );
}




function moveRule(rules: RuleEvaluation[], id: number, toPosition: number) {
  // this mirrors move_to in models.py
  // Move rule id to toPosition, shifting other rules as necessary.
  // If the target position is already taken, increase the position of all rules
  // above or equal to toPosition by 1.

  console.log("moveRule moving id", id, "to position:", toPosition);

  // const rules = evaluationResult.rules;
  const rule = rules.find((r) => r.id === id);
  if (!rule) {
    return rules;
  }

  if (rule.position == toPosition) {
    // notihing to do
    return rules;
  }

  const clamp = (num: number, min: number, max: number): number => Math.min(Math.max(num, min), max);
  const newPosition = clamp(toPosition, 1, rules.length);
  const curPosition = rule.position;
  if (newPosition > curPosition) {
    // moving down
    const newRules = rules.map((r) => {
      if (r.id === id) {
        return { ...r, position: newPosition };
      }
      if (r.position > curPosition && r.position <= newPosition) {
        return { ...r, position: r.position - 1 };
      }
      return r;
    });
    return newRules;
  } else {
    // moving up
    const newRules = rules.map((r) => {
      if (r.id === id) {
        return { ...r, position: newPosition };
      }
      if (r.position >= newPosition && r.position < curPosition) {
        return { ...r, position: r.position + 1 };
      }
      return r;
    });
    return newRules;
  }
}