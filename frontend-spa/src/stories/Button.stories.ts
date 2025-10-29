import type { Meta, StoryObj } from '@storybook/react-vite';
import { fn } from 'storybook/test';
import Button from '../Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    default: {
      control: 'boolean',
      description: 'Makes the button a default/primary button',
    },
    leftAlign: {
      control: 'boolean',
      description: 'Aligns the button content to the left',
    },
    disabled: {
      control: 'boolean',
      description: 'Disables the button',
    },
    children: {
      control: 'text',
      description: 'Button content',
    },
  },
  args: {
    onClick: fn(),
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: 'Standard Button',
  },
};

export const DefaultButton: Story = {
  args: {
    children: 'Default Button',
    default: true,
  },
};

export const LeftAligned: Story = {
  args: {
    children: 'Left Aligned Button',
    leftAlign: true,
  },
};

export const DefaultLeftAligned: Story = {
  args: {
    children: 'Default Left Aligned',
    default: true,
    leftAlign: true,
  },
};

export const Disabled: Story = {
  args: {
    children: 'Disabled Button',
    disabled: true,
  },
};

export const DisabledDefault: Story = {
  args: {
    children: 'Disabled Default Button',
    default: true,
    disabled: true,
  },
};

export const LongText: Story = {
  args: {
    children: 'Ein sehr langer Button-Text der möglicherweise umgebrochen wird',
  },
};

export const WithIcon: Story = {
  args: {
    children: '+ Neues Element hinzufügen',
    default: true,
  },
};

export const Small: Story = {
  args: {
    children: 'Klein',
    style: { fontSize: '14px', padding: '6px 12px' },
  },
};

export const Large: Story = {
  args: {
    children: 'Groß',
    style: { fontSize: '18px', padding: '12px 24px' },
  },
};
