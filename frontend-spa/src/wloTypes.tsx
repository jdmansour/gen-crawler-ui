
export type WloFieldType = "text" |
    "textarea" |
    "date" |
    "duration" |
    "singleoption" |
    "multivalueFixedBadges" |
    "multivalueSuggestBadges" |
    "multivalueTree" |
    "license" |
    "range";

export interface WloFieldValue {
    value: string;
    display: string;
}

export interface WloFieldValueNested extends WloFieldValue {
    parent?: WloFieldValueNested;
}

export interface WloLicenseFieldValue {
    url: string;
    // version: string;
    // description: string;
    icon_url: string | null;
    cc_key: string | null;
    cc_version: string | null;
}

export interface WloRangeFieldValue {
    min: number;
    max: number;
    display: string;
}

export type WloBaseFieldInfo = {
    id: string;
    type: WloFieldType;
    inheritable: boolean;
    recommended: boolean;
    caption: string;
    bottomCaption: string | null;
    placeholder: string | null;
};

export type WloFieldInfo =
    WloTextFieldInfo |
    WloSingleOptionFieldInfo |
    WloMultivalueFixedBadgesFieldInfo |
    WloMultivalueSuggestBadgesFieldInfo |
    WloMultivalueTreeFieldInfo |
    WloDateFieldInfo |
    WloDurationFieldInfo |
    WloLicenseFieldInfo |
    WloRangeFieldInfo;

export type WloTextFieldInfo = WloBaseFieldInfo & {
    type: "text" | "textarea";
    value?: string | null;
};

export type WloDateFieldInfo = WloBaseFieldInfo & {
    type: "date";
    value?: WloFieldValue | null;
};

export type WloDurationFieldInfo = WloBaseFieldInfo & {
    type: "duration";
    value?: WloFieldValue | null;
};

export type WloSingleOptionFieldInfo = WloBaseFieldInfo & {
    type: "singleoption";
    value?: WloFieldValue;
};

export type WloMultivalueFixedBadgesFieldInfo = WloBaseFieldInfo & {
    type: "multivalueFixedBadges";
    values: WloFieldValue[];
};

export type WloMultivalueSuggestBadgesFieldInfo = WloBaseFieldInfo & {
    type: "multivalueSuggestBadges";
    values: WloFieldValue[];
};

export type WloMultivalueTreeFieldInfo = WloBaseFieldInfo & {
    type: "multivalueTree";
    values: WloFieldValueNested[];
};

export type WloLicenseFieldInfo = WloBaseFieldInfo & {
    type: "license";
    value: WloLicenseFieldValue | null;
};

export type WloRangeFieldInfo = WloBaseFieldInfo & {
    type: "range";
    value: WloRangeFieldValue | null;
};

export function fieldMissing(field: WloFieldInfo) {
    switch (field.type) {
        case "text":
        case "textarea":
        case "date":
        case "duration":
        case "singleoption":
            return (field.value === undefined || field.value === null || field.value === "");
        case "multivalueFixedBadges":
        case "multivalueSuggestBadges":
        case "multivalueTree":
            return (field.values === undefined || field.values === null || field.values.length === 0);

    }
}
export type GroupInfo = {
    id: string;
    display: string;
    icon: string;
    fields: string[];
};
