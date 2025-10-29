import type { Meta, StoryObj } from '@storybook/react-vite';

import MetadataInheritancePage from './MetadataInheritancePage';
import { MemoryRouter } from 'react-router';
import SAMPLE_DATA from "./sampleData.json";
import { GroupInfo, WloFieldInfo } from './wloTypes';

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
    (Story) => (
      <MemoryRouter>
        <Story />
      </MemoryRouter>
    ),
  ],

};