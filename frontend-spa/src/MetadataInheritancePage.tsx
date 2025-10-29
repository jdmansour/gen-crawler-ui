
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
    }
) {
    const { fields, groups } = props;

    const navigate = useNavigate();
    const location = useLocation();
    const newCrawlerName = location.state?.newCrawlerName || "";

    //const selectedFields: string[] = ["ccm:oeh_profession_group"];
    const [selectedFields, setSelectedFields] = useState<string[]>([]);

    function setHistoryState(state: {
        step: CrawlerDashboardStep;
        newCrawlerName?: string;
    }) {
        const loc = "#" + state.step;
        navigate(loc, { state: state, replace: false });
    }

    function selectAllRecommendedFields() {
        const tmp = [...selectedFields];
        for (const field of fields) {
            const missing = fieldMissing(field);
            
            if (field.recommended && !missing) {
                if (!tmp.includes(field.id)) {
                    tmp.push(field.id);
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

            <WloFieldGroupSet groups={groups} fields={fields} selectedFields={selectedFields} />

            <div className="wlo-button-group">
                <Button leftAlign onClick={() => navigate(-1)}>
                    Zurück
                </Button>
                <Button
                    default
                    onClick={() =>
                        setHistoryState({
                            step: "filter-crawls",
                            newCrawlerName: newCrawlerName,
                        })
                    }
                >
                    Weiter
                </Button>
            </div>
        </div>
    </div>
}