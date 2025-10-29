// Custom element wrapping the Button component
import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import appCss from "../App.css?inline";
import App from "../App.tsx";
import breadcrumbsCss from "../Breadcrumbs.css?inline";
import buttonCss from "../Button.css?inline";
import filterTabsCss from "../FilterTabs.css?inline";
import indexCSS from "../index.css?inline";
import inputWithButtonCss from "../InputWithButton.css?inline";
import listViewCss from "../ListView.css?inline";
import sheetCss from "../Sheet.css?inline";
import siteLayoutCss from "../SiteLayout.css?inline";

// Wrap Button component in a custom element
class WLOGenCrawler extends HTMLElement {
  connectedCallback() {
    console.log("WLOGenCrawler connected");
    const shadowRoot = this.attachShadow({ mode: "open" });

    const mountPoint = document.createElement("div");
    shadowRoot.appendChild(mountPoint);

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
    addGlobalStyle(inputWithButtonCss);
    addGlobalStyle(sheetCss);
    addGlobalStyle(siteLayoutCss);
    addGlobalStyle(breadcrumbsCss);

    const basePath = this.getAttribute("base-path") || "";

    const root = ReactDOM.createRoot(mountPoint);
    root.render(
      <StrictMode>
        <BrowserRouter>
          <Routes>
            <Route path={basePath} element={<App />} />
          </Routes>
        </BrowserRouter>
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
