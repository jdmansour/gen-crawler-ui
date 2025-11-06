import type { Meta, StoryObj } from '@storybook/react-vite';
import TableTest from './TableTest';

const meta = {
  component: TableTest,
} satisfies Meta<typeof TableTest>;

export default meta;

type Story = StoryObj<typeof TableTest>;

export const Default: Story = {
  args: {
    theme: 'default'
  }
};

export const Rounded: Story = {
  args: {
    theme: 'rounded'
  }
};