import TextField, { TextFieldProps } from '@mui/material/TextField';
import type { Meta, StoryObj } from '@storybook/react-vite';
import MdsEditor from './MdsEditor';

const meta = {
  title: 'Components/MdsEditor',
  component: MdsEditor,
} satisfies Meta<typeof MdsEditor>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    title: "Hello World",
  },
  render: (args) => {
    const commonProps: TextFieldProps = {
        margin: 'normal',
        variant: 'filled',
        fullWidth: true,
        slotProps: { inputLabel: { shrink: true } }
    };
    
    return <MdsEditor {...args}>
      MDS Editor Placeholder
      <TextField label="Beschreibung" {...commonProps} />
      <TextField label="URL" helperText="Internetaddresse des Inhalts" {...commonProps} />
      <TextField label="Sprache(n)" {...commonProps} />
    </MdsEditor>
  }
};