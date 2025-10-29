
import { useLocation, useNavigate } from "react-router-dom";
import Button from "./Button";
import WloFieldGroupSet from "./WloFieldGroupSet";
import { CrawlerDashboardStep } from "./types";
import { GroupInfo, WloFieldInfo } from "./wloTypes";

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

    function setHistoryState(state: {
        step: CrawlerDashboardStep;
        newCrawlerName?: string;
    }) {
        const loc = "#" + state.step;
        navigate(loc, { state: state, replace: false });
    }

    return <div className="main-content">
        <div>
            <h2>Metadatenvererbung</h2>
            <p>Wähle die Felder aus, die von dem Quelldatensatz übernommen werden sollen.</p>

            <WloFieldGroupSet groups={groups} fields={fields} />

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