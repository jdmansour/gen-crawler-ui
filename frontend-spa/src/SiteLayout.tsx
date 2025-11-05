import "./SiteLayout.css";
import ShowSidebarIcon from "./assets/icons/show-sidebar.svg?react";
import CloseIcon from "./assets/icons/close.svg?react";
import { HTMLProps, useEffect, useRef, useState } from "react";

export default function SiteLayout(props: {
  children: React.ReactNode;
  sidebar?: React.ReactNode;
  sidebarVisible?: boolean;
  onSidebarClose?: () => void;
} & HTMLProps<HTMLDivElement>) {
  const { children, sidebar, onSidebarClose, ...otherProps } = props;
  const siteLayoutRef = useRef<HTMLDivElement>(null);
  let { sidebarVisible } = props;
  if (sidebarVisible == undefined) {
    sidebarVisible = true;
  }

  //const sidebarHeight = siteLayoutRef?.current?.clientHeight ? siteLayoutRef?.current?.clientHeight / 3 : undefined;
  // const [sidebarHeight, setSidebarHeight] = useState<number | undefined>(undefined);

  // useEffect(() => {
  //   if (siteLayoutRef.current) {
  //     const documentHeight = document.documentElement.clientHeight;
  //     const height = documentHeight - siteLayoutRef.current.clientTop;
  //     console.log("Setting sidebar height to:", height);
  //     setSidebarHeight(height);
  //   }
  // }, [siteLayoutRef]);

  return (
    <div
      className={
        "wlo-sitelayout" +
        (sidebarVisible ? " wlo-sitelayout-sidebar-visible" : "")
      }
      {...otherProps}
      ref={siteLayoutRef}
    >
      <main className="wlo-main">
        {children}
      </main>
      <Sidebar onClose={onSidebarClose} title="Generischer Crawler">
        {sidebar}
      </Sidebar>
    </div>
  );
}

export function Sidebar(
  props: {
    title: string;
    onClose?: () => void;
    children: React.ReactNode;
  } & React.HTMLAttributes<HTMLDivElement>,
) {
  return (
    <div className="wlo-sidebar" style={props.style} {...props}>
      <h2 className="wlo-sidebar-title">
        {props.title}
        <button onClick={props.onClose} className="wlo-sidebar-button">
          <CloseIcon width={24} />
        </button>
      </h2>
      <div>{props.children}</div>
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
