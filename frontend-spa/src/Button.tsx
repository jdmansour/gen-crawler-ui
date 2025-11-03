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
  // remove leftAlign and default from props to avoid React warnings
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { leftAlign, default: isDefault, ...buttonProps } = props;
  return (
    <button {...buttonProps} className={className}>
      {props.children}
    </button>
  );
}
