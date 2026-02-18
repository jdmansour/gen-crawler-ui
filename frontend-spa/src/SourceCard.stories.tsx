import type { Meta, StoryObj } from '@storybook/react-vite';
import SourceCard from './SourceCard';
import sourceItem from './fixtures/testSourceItem.json';

const meta = {
  component: SourceCard,
  tags: ['autodocs'],
} satisfies Meta<typeof SourceCard>;

export default meta;

type Story = StoryObj<typeof SourceCard>;

export const Default: Story = {
  args: {
    sourceItem: sourceItem,
  }
};

export const Horizontal: Story = {
  args: {
    sourceItem: sourceItem,
    orientation: "horizontal",
  }
};
