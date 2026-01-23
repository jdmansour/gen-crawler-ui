import type { Meta, StoryObj } from '@storybook/react-vite';

import InputWithButton from './InputWithButton';

const meta = {
  title: 'Components/InputWithButton',
  component: InputWithButton,
  tags: ['autodocs'],
} satisfies Meta<typeof InputWithButton>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {}
};