// Custom element wrapping the Button component
import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import appCss from "../App.css?inline";
import App from "../App.tsx";
import breadcrumbsCss from "../Breadcrumbs.css?inline";
import buttonCss from "../Button.css?inline";
import filterTabsCss from "../FilterTabs.css?inline";
import filterTabsModuleCss from "../FilterTabs.module.css?inline";
import indexCSS from "../index.css?inline";
import inputWithButtonCss from "../InputWithButton.css?inline";
import listViewCss from "../ListView.css?inline";
import sheetCss from "../Sheet.css?inline";
import siteLayoutCss from "../SiteLayout.css?inline";
import createCache from '@emotion/cache';
import { CacheProvider } from '@emotion/react';
import DashboardPage from "../DashboardPage.tsx";
import RootLayout from "../RootLayout.tsx";
import {MetadataInheritancePage, SelectSourcePage} from "../index.ts";
import AddCrawlerPage from "../AddCrawlerPage.tsx";
import FilterSetPage from "../FilterSetPage.tsx";
import CrawlerDetailsPage from "../CrawlerDetailsPage.tsx";
import { ApiUrlContext } from "../ApiUrlContext";


// Wrap Button component in a custom element
class WLOGenCrawler extends HTMLElement {
  connectedCallback() {
    console.log("WLOGenCrawler connected");
    const shadowRoot = this.attachShadow({ mode: "open" });

    const mountPoint = document.createElement("div");
    mountPoint.style.boxSizing = "border-box";
    mountPoint.style.height = "100%";
    mountPoint.style.display = "flex";
    mountPoint.style.flexDirection = "column";
    shadowRoot.appendChild(mountPoint);

    const cache = createCache({
      key: 'css',
      prepend: true,
      container: shadowRoot,
    });


    function addGlobalStyle(css: string) {
      const style = document.createElement("style");
      style.textContent = css;
      shadowRoot.appendChild(style);
    }
    // Add global styles to the shadow DOM
    addGlobalStyle(appCss);
    addGlobalStyle(indexCSS);
    addGlobalStyle(listViewCss);
    addGlobalStyle(buttonCss);
    addGlobalStyle(filterTabsCss);
    addGlobalStyle(filterTabsModuleCss);
    addGlobalStyle(inputWithButtonCss);
    addGlobalStyle(sheetCss);
    addGlobalStyle(siteLayoutCss);
    addGlobalStyle(breadcrumbsCss);

    const basePath = this.getAttribute("base-path") || "";
    const apiUrl = this.getAttribute("api-url") || "";

    const root = ReactDOM.createRoot(mountPoint);
    root.render(
        <StrictMode>
          <CacheProvider value={cache}>
            <ApiUrlContext.Provider value={apiUrl}>
            <BrowserRouter basename={basePath}>
              <Routes>
                <Route element={<RootLayout />} >
                  <Route index element={<DashboardPage />} />
                  <Route path="select-source" element={<SelectSourcePage />} />
                  <Route path="add-crawler" element={<AddCrawlerPage />} />
                  <Route path="crawlers/:crawlerId/metadata-inheritance" element={<MetadataInheritancePage />} />
                  <Route path="crawlers/:crawlerId/filters" element={<FilterSetPage csrfToken={"token"} />} />
                  <Route path="crawlers/:crawlerId" element={<CrawlerDetailsPage />} />
                </Route>
              </Routes>
            </BrowserRouter>
            </ApiUrlContext.Provider>
          </CacheProvider>
        </StrictMode>,
    );
  }
  disconnectedCallback() {
    // Cleanup if needed
  }
}
// Define the custom element
customElements.define("wlo-gen-crawler", WLOGenCrawler);
// Export the custom element for use in other files
export default WLOGenCrawler;
