
import { useLocation, useNavigate } from "react-router-dom";
import Button from "./Button";
import WloFieldGroupSet from "./WloFieldGroupSet";
import { CrawlerDashboardStep } from "./types";
import { fieldMissing, GroupInfo, WloFieldInfo } from "./wloTypes";
import { Button as MUIButton, FormGroup } from "@mui/material";
import { useState } from "react";

export default function MetadataInheritancePage(
    props: {
        fields: WloFieldInfo[];
        groups: GroupInfo[];
        onSave?: (selectedFields: Record<string, boolean>) => void;
    }
) {
    const { fields, groups, onSave } = props;

    const navigate = useNavigate();
    const location = useLocation();
    const newCrawlerName = location.state?.newCrawlerName || "";

    //const selectedFields: string[] = ["ccm:oeh_profession_group"];
    const [selectedFields, setSelectedFields] = useState<Record<string, boolean>>({});

    function setHistoryState(state: {
        step: CrawlerDashboardStep;
        newCrawlerName?: string;
    }) {
        const loc = "#" + state.step;
        navigate(loc, { state: state, replace: false });
    }

    function selectAllRecommendedFields() {
        const tmp = {...selectedFields};
        for (const field of fields) {
            console.log("Checking field:", field.id);
            const missing = fieldMissing(field);
            
            if (field.recommended && !missing) {
                if (!tmp[field.id]) {
                    tmp[field.id] = true;
                }
            }
        }
        setSelectedFields(tmp);
    }

    return <div className="main-content">
        <div>
            <h2>Metadatenvererbung</h2>
            <p>Dein neuer Crawler wurde erstellt! Während im Hintergrund die Quelle analysiert wird, kannst du jetzt schon mal die Felder auswählen, die von dem Quelldatensatz übernommen werden sollen.</p>
            <FormGroup style={{ marginBottom: "1em" }}>
                <MUIButton onClick={selectAllRecommendedFields}>Alle empfohlenen Felder auswählen</MUIButton>
            </FormGroup>

            <WloFieldGroupSet groups={groups} fields={fields} selectedFields={selectedFields} onSelectedFieldsChange={
                (update) => {
                    console.log("Field selection update:", update);
                    setSelectedFields(prev => {
                        return { ...prev, ...update };
                    });
                }}
            />

            <div className="wlo-button-group">
                <Button leftAlign onClick={() => navigate(-1)}>
                    Zurück
                </Button>
                <Button
                    default
                    onClick={() => {
                        // console.log("Selected fields:", selectedFields);
                        onSave?.(selectedFields);
                    }
                        // setHistoryState({
                        //     step: "filter-crawls",
                        //     newCrawlerName: newCrawlerName,
                        // })
                    }
                >
                    Weiter
                </Button>
            </div>
        </div>
    </div>
}