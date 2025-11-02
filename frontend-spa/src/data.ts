import { Crawler } from "./apitypes";

export const crawlerList: Crawler[] = [
  {
    id: 1,
    name: "Wikipedia",
    status: "draft",
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    source_item: "source-1",
    start_url: "https://de.wikipedia.org/wiki/Wikipedia:Hauptseite",
    inherited_fields: [],
    crawl_jobs: [],
  },
  {
    id: 2,
    name: "Leifi Physik",
    status: "pending",
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    source_item: "source-2",
    start_url: "https://www.leifiphysik.de/",
    inherited_fields: [],
    crawl_jobs: []
  },
  {
    id: 3,
    name: "Klexikon",
    status: "stopped",
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    source_item: "source-3",
    start_url: "https://klexikon.zum.de/",
    inherited_fields: [],
    crawl_jobs: []
  },
  {
    id: 4,
    name: "Arbeitsagentur",
    status: "error",
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    source_item: "source-4",
    start_url: "https://www.arbeitsagentur.de/",
    inherited_fields: [],
    crawl_jobs: []
  },
  {
    id: 5,
    name: "Physik im Advent",
    status: "published",
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    source_item: "source-5",
    start_url: "https://www.physik-im-advent.de/",
    inherited_fields: [],
    crawl_jobs: []
  },
];
