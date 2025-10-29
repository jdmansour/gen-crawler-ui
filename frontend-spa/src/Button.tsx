import React from "react";
import './Button.css';

export default function Button(
  props: {
    children: React.ReactNode;
    default?: boolean;
    leftAlign?: boolean;
  } & React.ButtonHTMLAttributes<HTMLButtonElement>,
) {
  let className = "wlo-button";
  if (props.className) {
    className += " " + props.className;
  }
  if (props.default) {
    className += " wlo-button-default";
  }
  if (props.leftAlign) {
    className += " wlo-button-left-align";
  }
  return (
    <button {...props} className={className}>
      {props.children}
    </button>
  );
}
