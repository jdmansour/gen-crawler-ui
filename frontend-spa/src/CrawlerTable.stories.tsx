import type { Meta, StoryObj } from '@storybook/react-vite';

import CrawlerTable from './CrawlerTable';

const meta = {
  component: CrawlerTable,
} satisfies Meta<typeof CrawlerTable>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    theme: 'rounded',
  }
};