// Custom element wrapping the Button component
import Button from "../Button.tsx";
// import React from 'react';
import ReactDOM from "react-dom/client";
import buttonCSS from "../Button.css?inline";
import indexCSS from "../index.css?inline";

// Wrap Button component in a custom element
class WLOButton extends HTMLElement {
  connectedCallback() {
    const shadowRoot = this.attachShadow({ mode: "open" });

    const mountPoint = document.createElement("div");
    shadowRoot.appendChild(mountPoint);

    function addGlobalStyle(css: string) {
      const style = document.createElement("style");
      style.textContent = css;
      shadowRoot.appendChild(style);
    }
    // Add global styles to the shadow DOM
    addGlobalStyle(buttonCSS);
    addGlobalStyle(indexCSS);

    const label = this.getAttribute("label") || "Click me";
    const defaultAttr = this.getAttribute("default");
    const default_ = defaultAttr !== null && defaultAttr !== "false";
    const root = ReactDOM.createRoot(mountPoint);
    root.render(
      <Button onClick={() => alert("Button clicked!")} default={default_}>
        {label}
      </Button>,
    );
  }
  disconnectedCallback() {
    // Cleanup if needed
  }
}
// Define the custom element
customElements.define("wlo-button", WLOButton);
// Export the custom element for use in other files
export default WLOButton;
