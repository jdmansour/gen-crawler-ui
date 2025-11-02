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

export type CrawlerStatus = "draft" |
  "pending" |
  "stopped" |
  "error" |
  "published";
