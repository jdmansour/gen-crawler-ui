import type { Meta, StoryObj } from '@storybook/react-vite';

import DashboardPage from './DashboardPage';
import { MemoryRouter } from 'react-router-dom';
import { crawlerList } from './data';

const meta = {
  title: 'Pages/DashboardPage',
  component: DashboardPage,
} satisfies Meta<typeof DashboardPage>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    crawlerList: crawlerList
  },
  decorators: [
    (Story) => (
      <MemoryRouter>
        <Story />
      </MemoryRouter>
    ),
  ],
};