import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import RootLayout from "./RootLayout.tsx";
import DashboardPage from "./DashboardPage.tsx";
import AddCrawlerPage from "./AddCrawlerPage.tsx";
import SelectSourcePage from "./SelectSourcePage.tsx";
import MetadataInheritancePage from "./MetadataInheritancePage.tsx";
import CrawlerDetailsPage from "./CrawlerDetailsPage.tsx";
import FilterSetPage from "./FilterSetPage.tsx";
import WloFakeHeader from "./WloFakeHeader.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<><WloFakeHeader /><RootLayout /></>} >
          <Route index element={<DashboardPage />} />
          <Route path="select-source" element={<SelectSourcePage />} />
          <Route path="add-crawler" element={<AddCrawlerPage />} />
          <Route path="crawlers/:crawlerId/metadata-inheritance" element={<MetadataInheritancePage />} />
          <Route path="crawlers/:crawlerId/filters" element={<FilterSetPage csrfToken={"token"} />} />
          <Route path="crawlers/:crawlerId" element={<CrawlerDetailsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);
