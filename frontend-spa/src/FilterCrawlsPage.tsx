import { useNavigate } from "react-router-dom";
import Button from "./Button";

export default function FilterCrawlsPage() {
    const navigate = useNavigate();
    return (
        <div className="main-content">
            <div>
                <h2>Filtereinstellungen</h2>
                <div className="wlo-button-group">
                    <Button leftAlign onClick={() => navigate(-1)}>
                        Zurück
                    </Button>
                </div>
            </div>
        </div>
    );
}