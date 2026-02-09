import type { Meta, StoryObj } from '@storybook/react-vite';
import SitemapTree from './SitemapTree';

const meta = {
  component: SitemapTree,
} satisfies Meta<typeof SitemapTree>;

export default meta;

type Story = StoryObj<typeof SitemapTree>;

export const Default: Story = {
  args: {
    // theme: 'default'
  }
};
