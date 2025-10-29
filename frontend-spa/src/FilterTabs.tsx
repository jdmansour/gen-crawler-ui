import { CustomIcon } from "./CustomIcon";
import styles from "./FilterTabs.module.css";
import FilterIcon from "./assets/icons/filter.svg?react";
import React, { useState, useEffect, useRef } from "react";

export type TabsStyle = "filter" | "sidebar";

export type TabInfo = {
  label: string;
  // string or component
  icon?: string | React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
  tag?: string;
};

let lastWheelTime = 0;
type WheelEventType = "wheel" | "touchpad";
let identifiedWheelEventType: WheelEventType | null = null;

function onWheel(event: WheelEvent) {
  // If using a scroll wheel, scroll horizontally
  if (event.currentTarget) {
    // if the last event is more than 300ms ago, reset type
    if (Date.now() - lastWheelTime > 300) {
      identifiedWheelEventType = null;
    }
    if (identifiedWheelEventType === null) {
      // small values < 48 are touchpad, larger values are scroll wheel
      identifiedWheelEventType =
        Math.abs(event.deltaY) < 48 ? "touchpad" : "wheel";
    }
    lastWheelTime = Date.now();
    if (identifiedWheelEventType === "wheel") {
      (event.currentTarget as HTMLDivElement).scrollLeft += event.deltaY * 2;
      event.preventDefault();
      event.stopPropagation();
    }
  }
}

export default function FilterTabs(props: {
  tabs: TabInfo[];
  onTabClick?: (index: number) => void;
  selectedTab?: number;
  tabsClickable?: "all" | "complete";
  style?: TabsStyle;
}) {
  const [indicatorLeft, setIndicatorLeft] = useState(0);
  const [indicatorWidth, setIndicatorWidth] = useState(0);
  const listRef = useRef<HTMLUListElement>(null);
  const divRef = useRef<HTMLDivElement>(null);
  const style = props.style ?? "filter";
  const tabsClickable = props.tabsClickable ?? "all";

  useEffect(() => {
    if (!listRef.current) return;
    const listItem = listRef.current.querySelector(
      "li.active",
    ) as HTMLLIElement | null;
    if (!listItem) return;
    const listItemRect = listItem.getBoundingClientRect();
    const listRect = listRef.current.getBoundingClientRect();
    if (indicatorWidth === 0) {
      // temporarily disable animation on listItem when
      // first loading
      const indicator = listRef.current.querySelector(
        `.${styles.indicator}`,
      ) as HTMLDivElement;
      inhibitAnimation(indicator);
    }
    setIndicatorLeft(listItemRect.left - listRect.left);
    setIndicatorWidth(listItemRect.width);

    listItem.scrollIntoView({ block: "nearest", inline: "nearest" });
  }, [props.selectedTab, props.tabs, indicatorWidth]);

  useEffect(() => {
    if (divRef.current) {
      divRef.current.addEventListener("wheel", onWheel, { passive: false });
    }
  }, []);

  function closeMenu() {
    const checkbox = document.getElementById(
      "wlo-filtertabs-toggle",
    ) as HTMLInputElement;
    if (checkbox) {
      checkbox.checked = false;
    }
  }

  let classNames = styles.wloFiltertabs;
  if (style === "sidebar") {
    classNames += ` ${styles.wloFiltertabsSidebar}`;
  }

  function tabComplete(index: number) {
    return index < (props.selectedTab ?? 0);
  }

  function tabClickable(index: number) {
    return (
      tabsClickable === "all" ||
      (tabsClickable === "complete" && tabComplete(index))
    );
  }

  return (
    <div className={classNames} ref={divRef}>
      <input
        type="checkbox"
        id="wlo-filtertabs-toggle"
        className={styles.wloFiltertabsMenuCheckbox}
      />
      <label htmlFor="wlo-filtertabs-toggle" className={styles.wloFiltertabsToggle}>
        <FilterIcon height={24} />
      </label>
      <div className={styles.wloFiltertabsMenu} onClick={closeMenu}>
        <ul ref={listRef}>
          {props.tabs.map((tab, index) => (
            <TabLabel
              active={index === props.selectedTab}
              key={index}
              label={tab.label}
              icon={tab.icon}
              clickable={tabClickable(index)}
              complete={style == "sidebar" && index < (props.selectedTab ?? 0)}
              onClick={() => {
                if (props.onTabClick) {
                  props.onTabClick(index);
                }
              }}
            />
          ))}
          <div
            className={styles.indicator}
            style={{
              left: indicatorLeft,
              width: indicatorWidth,
            }}
          />
        </ul>
      </div>
    </div>
  );
}

function inhibitAnimation(indicator: HTMLElement) {
  indicator.style.transition = "none";
  setTimeout(() => {
    indicator.style.transition = "";
  }, 100);
}

function TabLabel(props: {
  label: string;
  icon?: string | React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
  active?: boolean;
  complete?: boolean;
  clickable?: boolean;
  onClick?: () => void;
}) {
  let classNames = "";
  if (props.active) {
    classNames += " active";
  }
  if (props.complete) {
    classNames += ` ${styles.wloFiltertabsTabComplete}`;
  }
  if (!props.clickable) {
    classNames += ` ${styles.wloFiltertabsTabDisabled}`;
  }
  return (
    <li className={classNames}>
      <a
        href="#"
        onClick={(event) => {
          if (props.clickable && props.onClick) {
            props.onClick();
          }
          event.preventDefault();
        }}
      >
        {typeof props.icon === "string" ? (
          <CustomIcon iconName={props.icon} />
          // <img src={props.icon} className={styles.icon} height={24} />
        ) : (
          props.icon &&
          React.createElement(props.icon, { className: styles.icon, height: 24 })
        )}
        {/* {props.icon && <img src={props.icon} className="icon" height={24} />} */}
        <span>{props.label}</span>
      </a>
    </li>
  );
}
