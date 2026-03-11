// Custom element wrapping the Button component
import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import appCss from "../App.css?inline";
import breadcrumbsCss from "../Breadcrumbs.css?inline";
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
import SourceDetailsSidebar from "../SourceDetailsSidebar.tsx";
import Api from "../api.ts";
import SourceDetailsSidebarHost from "../SourceDetailsSidebarHost.tsx";


// Wrap Button component in a custom element
class WLOGenCrawlerSidebar extends HTMLElement {
  connectedCallback() {
    console.log("WLOGenCrawlerSidebar connected");
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
    addGlobalStyle(filterTabsCss);
    addGlobalStyle(filterTabsModuleCss);
    addGlobalStyle(inputWithButtonCss);
    addGlobalStyle(sheetCss);
    addGlobalStyle(siteLayoutCss);
    addGlobalStyle(breadcrumbsCss);

    const basePath = this.getAttribute("base-path") || "";
    const apiUrl = this.getAttribute("api-url") || "";

    const sourceGuid = this.getAttribute("source-guid") || undefined;
    

    const root = ReactDOM.createRoot(mountPoint);
    root.render(
        <StrictMode>
          <CacheProvider value={cache}>
            <ApiUrlContext.Provider value={apiUrl}>
              <SourceDetailsSidebarHost sourceGuid={sourceGuid} basePath={basePath} />
            </ApiUrlContext.Provider>
          </CacheProvider>
        </StrictMode>,
    );
  }
  disconnectedCallback() {
    // Cleanup if needed
  }
  // handle attribute changed
  static get observedAttributes() {
    return ["base-path", "source-guid"];
  }
  attributeChangedCallback(name: string, oldValue: string | null, newValue: string | null) {
    if ((name === "source-guid" || name === "base-path") && oldValue !== newValue) {
      const sourceGuid = this.getAttribute("source-guid") || undefined;
      const basePath = this.getAttribute("base-path") || "";
      const apiUrl = this.getAttribute("api-url") || "";
      const mountPoint = this.shadowRoot?.querySelector("div") as HTMLElement
      const cache = createCache({ key: 'css', prepend: true, container: this.shadowRoot });

      const root = ReactDOM.createRoot(mountPoint);
      root.render(
        <StrictMode>
          <CacheProvider value={cache}>
            <ApiUrlContext.Provider value={apiUrl}>
              <SourceDetailsSidebarHost sourceGuid={sourceGuid} basePath={basePath} />
            </ApiUrlContext.Provider>
          </CacheProvider>
        </StrictMode>,
      );
    }
  }
}
// Define the custom element
customElements.define("wlo-gen-crawler-sidebar", WLOGenCrawlerSidebar);
// Export the custom element for use in other files
export default WLOGenCrawlerSidebar;
