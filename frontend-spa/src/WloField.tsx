import { Chip, Typography } from "@mui/material";
import { WloFieldInfo, WloSingleOptionFieldInfo, WloMultivalueFixedBadgesFieldInfo, WloMultivalueSuggestBadgesFieldInfo, WloMultivalueTreeFieldInfo, WloLicenseFieldInfo, WloFieldValueNested } from "./wloTypes";

export default function WloField(props: { field: WloFieldInfo }) {
    const { field } = props;

    switch (field.type) {
        case "text":
        case "textarea":
        case "duration":
        case "date":
            return <WloTextField field={field} />;

        case "multivalueFixedBadges":
        case "multivalueTree":
        case "multivalueSuggestBadges":
            return <WloMultivalueField field={field} />;

        case "singleoption":
            return <WloSingleoptionField field={field} />;

        case "license":
            return <WloLicenseField field={field} />;

        case "range":
            return <WloTextField field={field} />;

        default:
            break;
    }
            
    // otherwise, render a placeholder for other field types
    return (
        <div style={{ paddingTop: '1.5em' }}>
            <div style={{ position: 'absolute', top: 0 }}><Typography variant="caption" color="textSecondary">{field.caption}</Typography></div>
            <div><Typography variant="body1">{getValueString(field)}</Typography></div>
            <div><Typography variant="caption" color="textSecondary">Field of type '{field.type}' is not implemented</Typography></div>
        </div>
    );
}

function WloSingleoptionField(props: { field: WloSingleOptionFieldInfo }) {
    const { field } = props;
    return <div style={{ paddingTop: '1.5em' }}>
        <div style={{ position: 'absolute', top: 0 }}><Typography variant="caption" color="textSecondary">{field.caption}</Typography></div>
        {field.value ? (
            <Chip key={field.value.value} label={field.value.display} style={{ marginRight: "0.5rem" }} />
        ) : (
            <Chip key="none" label="Kein(e)" style={{ marginRight: "0.5rem" }} variant="outlined" />
        )}
    </div>;
}

function WloMultivalueField(props: { field: WloMultivalueFixedBadgesFieldInfo | WloMultivalueSuggestBadgesFieldInfo | WloMultivalueTreeFieldInfo }) {
    const { field } = props;
    return <div style={{ paddingTop: '1.5em' }}>
        <div style={{ position: 'absolute', top: 0 }}><Typography variant="caption" color="textSecondary">{field.caption}</Typography></div>
        {field.values.length === 0 ? (
            <Chip key="none" label="Kein(e)" style={{ marginRight: "0.5rem" }} variant="outlined" />
        ) : (
            field.values.map((val) => (
                <Chip key={val.value} label={getTreeDisplay(val)} style={{ marginRight: "0.5rem" }} />
            ))
        )}
    </div>;
}

function WloTextField(props: { field: WloFieldInfo }) {
    const { field } = props;
    return <div style={{ paddingTop: '1.5em' }}>
        <div style={{ position: 'absolute', top: 0 }}><Typography variant="caption" color="textSecondary">{field.caption}</Typography></div>
        <div><Typography variant="body1">{getValueString(field)}</Typography></div>
    </div>;
}

function WloLicenseField(props: { field: WloLicenseFieldInfo }) {
    const { field } = props;
    const license = field.value;

    if (!license) {
        return (
            <div style={{ paddingTop: '1.5em' }}>
                <div style={{ position: 'absolute', top: 0 }}><Typography variant="caption" color="textSecondary">{field.caption}</Typography></div>
                <Typography variant="body1">Keine Lizenz angegeben</Typography>
            </div>
        );
    }

    let display = "Unbekannte Lizenz";
    let licenseGroup: string|null = null;
    if (license.cc_key && license.cc_version) {
        display = `${license.cc_key} (${license.cc_version})`;
        licenseGroup = "Creative Commons";
    }

    return (
        <div style={{ paddingTop: '1.5em' }}>
            <div style={{ position: 'absolute', top: 0 }}><Typography variant="caption" color="textSecondary">{field.caption}</Typography></div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1em' }}>
                {license.icon_url &&
                    <img src={license.icon_url} alt="License Icon" style={{ height: '1.5em' }} />
                }
                <div>
                    <Typography variant="body1"><a href={license.url}>{display}</a></Typography>
                    {licenseGroup &&
                    <Typography variant="caption" color="textSecondary">{licenseGroup}</Typography>
                    }
                </div>
            </div>
        </div>
    );

}

function getTreeDisplay(val: WloFieldValueNested): string {
    let res = val.display;
    if (val.parent) {
        res = getTreeDisplay(val.parent) + " > " + res;
    }
    return res;
}

function getValueString(field: WloFieldInfo): string {
    switch (field.type) {
        case "text":
        case "textarea":
            return field.value || "-";
        case "date":
        case "duration":
            return field.value?.display || "-";
        case "singleoption":
            return field.value?.display || "-";
        case "multivalueFixedBadges":
        case "multivalueSuggestBadges":
        case "multivalueTree":
            return field.values.map(v => v.display).join(", ");
        case "range":
            return field.value?.display || "-";
        default:
            return "";
    }
}
