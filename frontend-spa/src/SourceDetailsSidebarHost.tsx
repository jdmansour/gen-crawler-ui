import { Crawler, SourceItem } from "./apitypes";
import SourceDetailsSidebar from './SourceDetailsSidebar';
import { useCallback, useEffect, useState } from 'react';
import Api from './api';
import { useSidebarComponentContext } from "./SidebarComponentContext";


export default function SourceDetailsSidebarHost(params: { sourceGuid?: string }) {
  const [sourceItem, setSourceItem] = useState<SourceItem | undefined>(undefined);
  const [crawlers, setCrawlers] = useState<Crawler[]>([]);
  const sourceGuid = params.sourceGuid ?? "aa1f3e38-babf-42a9-9005-592b98bcb4ae";
  const {apiUrl} = useSidebarComponentContext();

  console.log("SourceDetailsSidebarHost rendering with sourceGuid:", sourceGuid);

  const loadData = useCallback(async function() {
    const api = new Api(apiUrl);
  
    try {
      console.log("SourceDetailsSidebarHost loadData triggered, fetching data...");
      const [source, crawlers] = await Promise.all([
        api.getSourceItem(sourceGuid),
        api.listCrawlers(),
      ]);
      console.log("Fetched source item:", source);
      console.log("Fetched crawlers:", crawlers);
      setSourceItem(source);
      const filteredCrawlers = crawlers.filter(c => c.source_item === sourceGuid);
      console.log("Filtered crawlers for sourceGuid:", filteredCrawlers);
      setCrawlers(filteredCrawlers);
    } catch (error) {
      console.error("Error fetching crawlers:", error);
      return [];
    }
  }, [apiUrl, sourceGuid]);

  useEffect(() => {
    console.log("SourceDetailsSidebarHost useEffect triggered, loading data...");
    loadData();
  }, [loadData]);

  return (
    <div>
      {/* <p>Crawler name: {sourceItem?.title}</p>
      <p>GUID: {sourceGuid}</p> */}
      <SourceDetailsSidebar sourceItem={sourceItem} crawlers={crawlers} />
    </div>
  );
  
}
