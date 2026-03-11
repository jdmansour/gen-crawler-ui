// Custom element wrapping the SourceDetailsSidebarHost component
import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
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
import { ApiUrlContext } from "../ApiUrlContext";
import SourceDetailsSidebarHost from "../SourceDetailsSidebarHost.tsx";


class WLOGenCrawlerSidebar extends HTMLElement {
  private root: ReactDOM.Root | null = null;
  private cache: ReturnType<typeof createCache> | null = null;

  connectedCallback() {
    console.log("WLOGenCrawlerSidebar connected");
    const shadowRoot = this.attachShadow({ mode: "open" });

    const mountPoint = document.createElement("div");
    mountPoint.style.boxSizing = "border-box";
    mountPoint.style.height = "100%";
    mountPoint.style.display = "flex";
    mountPoint.style.flexDirection = "column";
    shadowRoot.appendChild(mountPoint);

    this.cache = createCache({
      key: 'css',
      prepend: true,
      container: shadowRoot,
    });

    function addGlobalStyle(css: string) {
      const style = document.createElement("style");
      style.textContent = css;
      shadowRoot.appendChild(style);
    }
    addGlobalStyle(appCss);
    addGlobalStyle(indexCSS);
    addGlobalStyle(listViewCss);
    addGlobalStyle(filterTabsCss);
    addGlobalStyle(filterTabsModuleCss);
    addGlobalStyle(inputWithButtonCss);
    addGlobalStyle(sheetCss);
    addGlobalStyle(siteLayoutCss);
    addGlobalStyle(breadcrumbsCss);

    this.root = ReactDOM.createRoot(mountPoint);
    this.renderComponent();
  }

  disconnectedCallback() {
    this.root?.unmount();
    this.root = null;
  }

  static get observedAttributes() {
    return ["base-path", "source-guid", "api-url"];
  }

  attributeChangedCallback(_name: string, oldValue: string | null, newValue: string | null) {
    if (oldValue !== newValue && this.root) {
      this.renderComponent();
    }
  }

  private renderComponent() {
    const basePath = this.getAttribute("base-path") ?? "";
    const apiUrl = this.getAttribute("api-url") ?? "";
    const sourceGuid = this.getAttribute("source-guid") ?? undefined;

    this.root!.render(
      <StrictMode>
        <CacheProvider value={this.cache!}>
          <ApiUrlContext.Provider value={apiUrl}>
            <SourceDetailsSidebarHost sourceGuid={sourceGuid} basePath={basePath} />
          </ApiUrlContext.Provider>
        </CacheProvider>
      </StrictMode>
    );
  }
}

customElements.define("wlo-gen-crawler-sidebar", WLOGenCrawlerSidebar);
export default WLOGenCrawlerSidebar;
