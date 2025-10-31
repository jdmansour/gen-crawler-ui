import { useEffect } from "react";
import { useOutletContext } from "react-router-dom";
import { UseStepContext } from "./RootContext";

export type CrawlerDashboardStep =
  | "dashboard"
  | "select-source"
  | "add-crawler"
  | "metadata-inheritance"
  | "filter-crawls"
  | "crawler-details";

export function useStep(step: CrawlerDashboardStep) {
  const { setStep } = useOutletContext<UseStepContext>();
  useEffect(() => {
    console.log("Setting step to:", step);
    setStep(step);
  }, [setStep, step]);
}

export class CrawlerInfo {
  id: number;
  name: string;
  status: CrawlerStatus;
  updatedAt: Date;
  sourceItemGuid?: string;
  start_url?: string;
  constructor(
    id: number,
    name: string,
    status: CrawlerStatus,
    updatedAt: Date,
    sourceItemGuid?: string,
    start_url?: string
  ) {
    this.id = id;
    this.name = name;
    this.status = status;
    this.updatedAt = updatedAt;
    this.sourceItemGuid = sourceItemGuid;
    this.start_url = start_url;
  }
}

export type CrawlerStatus = "draft" |
  "pending" |
  "stopped" |
  "error" |
  "published";
