
import { FormGroup } from "@mui/material";
import InheritableWloField from "./InheritableWloField";
import MdsEditor from "./MdsEditor";
import { WloFieldInfo } from "./wloTypes";
import { CustomIcon } from "./CustomIcon";

export default function WloFieldGroup(props: {
    title: string, icon: string, fields: WloFieldInfo[],
    selectedFields?: string[],
    onSelectedFieldsChange?: (selectedFields: string[]) => void
}) {
    // const fieldNotMissing = (field: WloFieldInfo) => !fieldMissing(field);    
    const {title, icon, fields, selectedFields, onSelectedFieldsChange} = props;

    return <MdsEditor title={title} icon={<CustomIcon iconName={icon} />}>
        <FormGroup>
            {/* {fields.filter(fieldNotMissing).map(field => { */}
            {fields.map(field => {
                return <InheritableWloField
                            key={field.id} field={field}
                            selected={selectedFields?.includes(field.id) || false}
                            onSelectedChange={() => onSelectedFieldsChange?.([field.id])} />
            })}
        </FormGroup>
    </MdsEditor>
}


// TODO NEXT:
// - Add button: go through everything and select all recommended fields
// - make onSelectedFieldsChange return name AND new state... propagate that up
// - dump new selection to console
// - save to DB
// - PROFIT!
