import type { Meta, StoryObj } from '@storybook/react-vite';
import SitemapTree from './SitemapTree';
import omatheSiteTree from './fixtures/omathe_site_tree.json';
import serloSiteTree from './fixtures/serlo_site_tree.json';
import lehrerOnlineSiteTree from './fixtures/lehrer-online_site_tree.json';

const meta = {
  component: SitemapTree,
} satisfies Meta<typeof SitemapTree>;

export default meta;

type Story = StoryObj<typeof SitemapTree>;

export const Default: Story = {
  args: {
    items: omatheSiteTree,
  }
};

export const Serlo: Story = {
  args: {
    items: serloSiteTree,
  }
};

export const LehrerOnline: Story = {
  args: {
    items: lehrerOnlineSiteTree,
  }
};