import type { Meta, StoryObj } from '@storybook/react-vite';
import { CustomIcon } from './CustomIcon';

const iconNames = [
  "description",
  "school",
  "done_all",
  "copyright",
  "accessibility",
  "robot",
  "error",
  "edit",
  "pending",
  "stop",
];

const meta: Meta<typeof CustomIcon> = {
  title: 'Components/CustomIcon',
  component: CustomIcon,
};
export default meta;

type Story = StoryObj<typeof CustomIcon>;

export const AllIcons: Story = {
  render: () => (
    <div>
    <h3>Available Icons</h3>
    <div style={{
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))',
  gap: '1rem',
}}>
  {iconNames.map(name => (
    <div key={name} style={{ textAlign: 'center' }}>
      <CustomIcon iconName={name} />
      <div style={{ fontSize: 12, marginTop: 4 }}>{name}</div>
    </div>
  ))}
</div>
</div>
  ),
};
