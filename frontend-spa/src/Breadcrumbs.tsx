import HomeIcon from "./assets/icons/home.svg?react";
import PathSeparator from "./assets/icons/pathseparator.svg?react";
import "./Breadcrumbs.css";

export type Breadcrumb = {
  label: string;
  url?: string;
  temporary?: boolean;
};

export default function Breadcrumbs(props: { breadcrumbs: Array<Breadcrumb> }) {
  return (
    <nav>
      <ol className="wlo-breadcrumbs">
        {props.breadcrumbs.map((breadcrumb, index) => (
          <li key={index} className={breadcrumb.temporary ? "wlo-breadcrumbs-temporary" : ""}>
            {index > 0 && <PathSeparator />}
            <AOrSpan href={breadcrumb.url}>
              {index == 0 && (
                <HomeIcon
                  className="wlo-breadcrumbs-home-icon"
                  width="24px"
                  height="24px"
                />
              )}
              <span>{breadcrumb.label}</span>
            </AOrSpan>
          </li>
        ))}
      </ol>
    </nav>
  );
}

function AOrSpan(props: { href?: string; children: React.ReactNode }) {
  if (props.href !== undefined) {
    return <a href={props.href}>{props.children}</a>;
  } else {
    return <>{props.children}</>;
  }
}
