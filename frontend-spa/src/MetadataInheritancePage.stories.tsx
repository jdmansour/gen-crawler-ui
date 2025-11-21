import type { Meta, StoryObj } from '@storybook/react-vite';
import { MemoryRouter, Outlet, Route, Routes } from 'react-router-dom';
import MetadataInheritancePage from './MetadataInheritancePage';
import SAMPLE_DATA from "./sampleData.json";
import { GroupInfo, WloFieldInfo } from './wloTypes';
import { MetadataInheritancePageContext, UseStepContext } from './RootContext';

const meta = {
  title: 'Pages/MetadataInheritancePage',
  component: MetadataInheritancePage,
} satisfies Meta<typeof MetadataInheritancePage>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    fields: SAMPLE_DATA.fields as WloFieldInfo[],
    groups: SAMPLE_DATA.groups as GroupInfo[],
  },
  decorators: [
    (Story) => {
      const outletContext: MetadataInheritancePageContext & UseStepContext = {
        crawlerList: [],
        setStep: () => {},
      };
      return <WithOutletContext outletContext={outletContext}>
        <Story />
      </WithOutletContext>;
    }
  ],

};

function WithOutletContext<T>(props: { outletContext: T, children: React.ReactNode }) {
  return <MemoryRouter>
        <Routes>
          <Route path="/" element={<Outlet context={props.outletContext} />}>
            <Route index element={props.children} />
          </Route>
        </Routes>
      </MemoryRouter>;
}