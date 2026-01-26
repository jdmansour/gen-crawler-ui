import type { Meta, StoryObj } from '@storybook/react-vite';

import DashboardPage from './DashboardPage';
import { MemoryRouter, Outlet, Route, Routes } from 'react-router-dom';
import { crawlerList } from './data';
import { DashboardPageContext, UseStepContext } from './RootContext';

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
    (Story) => {
      const outletContext: DashboardPageContext & UseStepContext= {
        crawlerList: crawlerList,
        setCrawlerList: () => {},
        setSidebarVisible: () => {},
        setStep: () => {},
        setObservedCrawlerId: () => {},
      };
      return <MemoryRouter>
        <Routes>
          <Route path="/" element={<Outlet context={outletContext} />}>
            <Route index element={<Story />} />
          </Route>
        </Routes>
      </MemoryRouter>;
    }
  ],
};