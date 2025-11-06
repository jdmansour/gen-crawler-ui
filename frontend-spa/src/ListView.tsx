import { HTMLProps } from "react";
import "./ListView.css";

export default function ListView(props: { children: React.ReactNode } & HTMLProps<HTMLTableElement>) {
  return (
    <table className="wlo-listview" {...props}>
      <tbody>{props.children}</tbody>
    </table>
  );
}
