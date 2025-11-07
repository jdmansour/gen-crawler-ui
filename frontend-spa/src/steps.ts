import { useEffect } from "react";
import { useOutletContext } from "react-router-dom";
import { UseStepContext } from "./RootContext";

export type CrawlerDashboardStep =
  | "dashboard"
  | "select-source"
  | "add-crawler"
  | "metadata-inheritance"
  | "filter-crawls"
  | "crawler-details"
  | "filters";

export function useStep(step: CrawlerDashboardStep) {
  const { setStep } = useOutletContext<UseStepContext>();
  useEffect(() => {
    setStep(step);
  }, [setStep, step]);
}


