import { createContext, HTMLProps, useContext, useRef } from "react";
import "./SiteLayout.css";
import CloseIcon from "./assets/icons/close.svg?react";
import ShowSidebarIcon from "./assets/icons/show-sidebar.svg?react";

const SidebarContext = createContext<{ onClose?: () => void }>({});

export function SidebarCloseButton() {
  const { onClose } = useContext(SidebarContext);
  return (
    <button onClick={onClose} className="wlo-sidebar-button">
      <CloseIcon width={24} />
    </button>
  );
}

export function SidebarTitle(props: { children: React.ReactNode }) {
  return (
    <h2 className="wlo-sidebar-title">
      {props.children}
      <SidebarCloseButton />
    </h2>
  );
}

export default function SiteLayout(props: {
  children: React.ReactNode;
  sidebarVisible: boolean;
  onSidebarClose?: () => void;
} & HTMLProps<HTMLDivElement>) {
  const { children, onSidebarClose, sidebarVisible, ...otherProps } = props;
  const siteLayoutRef = useRef<HTMLDivElement>(null);

  let className = "wlo-sitelayout";
  if (sidebarVisible) {
    className += " wlo-sitelayout-sidebar-visible";
  }

  return (
    <div className={className} {...otherProps} ref={siteLayoutRef}>
      <SidebarContext.Provider value={{ onClose: onSidebarClose }}>
        <main className="wlo-main">
          {children}
        </main>
        <div className="wlo-sidebar">
          <div id="sidebar-outlet"></div>
        </div>
      </SidebarContext.Provider>
    </div>
  );
}

export function ShowSidebarButton(
  props: {
    onClick: () => void;
  } & React.HTMLAttributes<HTMLButtonElement>,
) {
  return (
    <button {...props} className="wlo-sidebar-button" onClick={props.onClick}>
      <ShowSidebarIcon width={24} />
    </button>
  );
}
