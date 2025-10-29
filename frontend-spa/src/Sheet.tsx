import React from "react";
import "./Sheet.css";
import CloseIcon from "./assets/icons/close.svg?react";

function Sheet(
  props: {
    children: React.ReactNode;
    className?: string;
    visible: boolean;
    onClose?: () => void;
  } & React.HTMLAttributes<HTMLDivElement>,
) {
  return (
    <div
      className="wlo-sheet-backdrop"
      style={{
        opacity: props.visible ? 1 : 0,
        pointerEvents: props.visible ? "all" : "none",
      }}
      onClick={props.onClose}
    >
      <div className="wlo-sheet-content" onClick={(e) => e.stopPropagation()}>
        <button className="wlo-sheet-close-button" onClick={props.onClose}>
          <CloseIcon width={24} />
        </button>
        {props.children}
      </div>
    </div>
  );
}
export default Sheet;
