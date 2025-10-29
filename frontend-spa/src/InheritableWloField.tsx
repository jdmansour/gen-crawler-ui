import { FormControlLabel, Checkbox } from "@mui/material";
import WloField from "./WloField";
import { WloFieldInfo, fieldMissing } from "./wloTypes";
import { Star } from "@mui/icons-material";

function MyFormControlLabel(props: React.ComponentProps<typeof FormControlLabel>) {
    return <FormControlLabel {...props} disableTypography style={{ marginRight: 0, marginLeft: 0, alignItems: 'center', width: '100%' }} />;
    return <FormControlLabel {...props} disableTypography style={{ marginRight: 0, marginLeft: 0, alignItems: 'baseline', width: '100%' }} />;
}

function MyCheckbox(props: React.ComponentProps<typeof Checkbox>) {
    // return <Checkbox {...props} />;
    return <Checkbox {...props} style={{ top: '0.45em' }} />;
}

export default function InheritableWloField(props: { field: WloFieldInfo, selected?: boolean, onSelectedChange?: (selected: boolean) => void }) {
    const { field } = props;

    const inheritable = (field.inheritable === undefined) ? true : field.inheritable;
    const recommended = (field.recommended === undefined) ? false : field.recommended;
    const missing = fieldMissing(field);
    
    return <div style={{ position: "relative", width: "100%", marginTop: '8px', marginBottom: '0px', verticalAlign: "top" }}>
        {(!inheritable) ? (
            <div style={{ marginLeft: 42 }}><WloField field={field} /></div>
        ) : (
            <MyFormControlLabel
                control={<MyCheckbox checked={props.selected} onChange={(event) => props.onSelectedChange?.(event.target.checked)} />}
                label={<WloField field={field} />}
            />
        )}

        {(inheritable && recommended && !missing) && (<>
            <div style={{
                position: "absolute", top: 0, right: 0,
                width: 0, height: 0,
                borderStyle: "solid",
                borderWidth: "0 42px 42px 0",
                borderColor: "transparent #ec4a70 transparent transparent",
                pointerEvents: "none",
            }} />
            <Star style={{
                position: "absolute", top: 4, right: 4,
                color: "white",
                width: 16,
                height: 16,
                pointerEvents: "none",
            }} />
        </>)
        }
    </div>;
}