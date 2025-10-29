import "./ListView.css";

export default function ListView(props: { children: React.ReactNode }) {
  return (
    <table className="wlo-listview">
      <tbody>{props.children}</tbody>
    </table>
  );
}
