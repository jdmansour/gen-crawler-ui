
import { FormGroup } from "@mui/material";
import InheritableWloField from "./InheritableWloField";
import MdsEditor from "./MdsEditor";
import { WloFieldInfo } from "./wloTypes";
import { CustomIcon } from "./CustomIcon";

export default function WloFieldGroup(props: { title: string, icon: string, fields: WloFieldInfo[] }) {
    // const fieldNotMissing = (field: WloFieldInfo) => !fieldMissing(field);    

    return <MdsEditor title={props.title} icon={<CustomIcon iconName={props.icon} />}>
        <FormGroup>
            {/* {props.fields.filter(fieldNotMissing).map(field => { */}
            {props.fields.map(field => {
                return <InheritableWloField key={field.id} field={field} />
            })}
        </FormGroup>
    </MdsEditor>
}
