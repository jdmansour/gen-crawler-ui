


export default function RuleTable(props: {rules: any, onDelete: (id: number) => void, onAdd: (id: number) => void}) {


    return <table className="table">
      <thead>
          <tr>
            <th>URL Pattern</th>
            <th>Matches</th>
            <th>Include</th>
            <th>Type</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          {props.rules.map((rule: any) => {
            return <tr key={rule.id}>
              <td>{rule.rule}</td>
              <td>{rule.count}</td>
              <td>{rule.include ? 'Yes' : 'No'}</td>
              <td>{rule.page_type}</td>
              <td>
                <button className="mybutton mybutton-table" onClick={(e) => props.onDelete(rule.id)}>x</button>
                <button className="mybutton mybutton-table" onClick={(e) => props.onAdd(rule.id)}>+</button>
              </td>
            </tr>
          })}
          </tbody>
        </table>
  }