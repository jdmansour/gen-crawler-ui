
import React from 'react';

export function myTest() {
    console.log("test");
  }

import Button from '../src/Button.tsx';

// Wrap the react component Button in a custom element
class WLOButton extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.button = React.createElement(Button, { label: this.getAttribute('label') });
    }

    connectedCallback() {
        React.render(this.button, this.shadowRoot);
    }

    disconnectedCallback() {
        React.unmountComponentAtNode(this.shadowRoot);
    }
}
// Define the custom element
customElements.define('wlo-button', WLOButton);
