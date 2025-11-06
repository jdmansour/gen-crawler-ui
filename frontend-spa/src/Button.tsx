import React from "react";
import './Button.css';

import FormControlLabel from '@mui/material/FormControlLabel';
import Button1 from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Link from '@mui/material/Link';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';

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
