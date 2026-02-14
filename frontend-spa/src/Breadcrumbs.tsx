import { Link } from "react-router-dom";
import HomeIcon from "./assets/icons/home.svg?react";
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
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
          <li key={index} className={breadcrumb.temporary ? "wlo-breadcrumbs-temporary" : ""} style={{display:"contents"}}>
            {index > 0 && <ChevronRightIcon sx={{ fontSize: 24, mt: "-2px" }} />}
            <LinkOrSpan href={breadcrumb.url}>
              {index == 0 && (
                <HomeIcon
                  className="wlo-breadcrumbs-home-icon"
                  width="24px"
                  height="24px"
                />
              )}
              <span>{breadcrumb.label}</span>
            </LinkOrSpan>
          </li>
        ))}
      </ol>
    </nav>
  );
}

function LinkOrSpan(props: { href?: string; children: React.ReactNode }) {
  if (props.href !== undefined) {
    return <Link to={props.href}>{props.children}</Link>;
  } else {
    return <>{props.children}</>;
  }
}
