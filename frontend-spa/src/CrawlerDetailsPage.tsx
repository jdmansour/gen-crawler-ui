import { useOutletContext, useParams } from "react-router-dom";
import { CrawlerDetailsPageContext } from "./RootContext";
import { useStep } from "./types";


export default function CrawlerDetailsPage() {
    const { crawlerId } = useParams();
    const { crawlerList } = useOutletContext<CrawlerDetailsPageContext>();
    const crawler = crawlerList.find(c => c.id.toString() === crawlerId);

    useStep("crawler-details");

    if (!crawlerId || !crawler) {
        return <div>Crawler not found</div>;
    }
    return <div>Crawler Details Page Number: {crawler.name} </div>;
}