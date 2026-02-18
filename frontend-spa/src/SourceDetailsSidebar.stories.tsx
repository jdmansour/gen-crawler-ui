import type { Meta, StoryObj } from '@storybook/react-vite';
import { MemoryRouter } from 'react-router-dom';
import { Crawler } from './apitypes';
import sourceItem from './fixtures/testSourceItem.json';
import SourceDetailsSidebar from './SourceDetailsSidebar';

const SOURCE_GUID = sourceItem.guid;

const mockCrawlers: Crawler[] = [
  {
    id: 1,
    name: "Klexikon Explorer",
    simple_state: "idle",
    state: "READY_FOR_CONTENT_CRAWL",
    created_at: new Date(Date.now() - 86400000 * 3).toISOString(),
    updated_at: new Date(Date.now() - 3600000).toISOString(),
    source_item: SOURCE_GUID,
    start_url: "https://klexikon.zum.de/",
    inherited_fields: [],
    crawl_jobs: [],
    url: "",
    filter_set_id: 1,
    filter_set_url: null,
  },
  {
    id: 2,
    name: "Klexikon Content",
    simple_state: "running",
    state: "CONTENT_CRAWL_RUNNING",
    created_at: new Date(Date.now() - 86400000).toISOString(),
    updated_at: new Date(Date.now() - 600000).toISOString(),
    source_item: SOURCE_GUID,
    start_url: "https://klexikon.zum.de/wiki/Hauptseite",
    inherited_fields: ["title", "description"],
    crawl_jobs: [],
    url: "",
    filter_set_id: 2,
    filter_set_url: null,
  },
];

const meta = {
  component: SourceDetailsSidebar,
  tags: ['autodocs'],
  decorators: [
    (Story) => (
      <MemoryRouter>
        <Story />
      </MemoryRouter>
    ),
  ],
} satisfies Meta<typeof SourceDetailsSidebar>;

export default meta;

type Story = StoryObj<typeof meta>;

export const WithCrawlers: Story = {
  args: {
    sourceGuid: SOURCE_GUID,
    sourceItem: sourceItem,
    crawlers: mockCrawlers,
  },
};

export const NoCrawlers: Story = {
  args: {
    sourceGuid: SOURCE_GUID,
    sourceItem: sourceItem,
    crawlers: [],
  },
};
