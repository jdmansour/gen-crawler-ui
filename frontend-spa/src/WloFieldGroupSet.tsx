import { Grid } from "@mui/system";
import WloFieldGroup from "./WloFieldGroup";
import { GroupInfo, WloFieldInfo } from "./wloTypes";

export default function WloFieldGroupSet(props: { groups: GroupInfo[], fields: WloFieldInfo[] }) {
    return (
        <Grid container spacing={2}>
            {props.groups.map(group => (
                <Grid size={{ xs: 12, md: group.id === 'general' ? 12 : 6 }}>
                    <WloFieldGroup key={group.id} title={group.display} icon={group.icon} fields={props.fields.filter(field => group.fields.includes(field.id))} />
                </Grid>
            ))}
        </Grid>
    );
}
