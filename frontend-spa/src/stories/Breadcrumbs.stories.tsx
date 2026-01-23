import type { Meta, StoryObj } from '@storybook/react-vite';
import { MemoryRouter } from 'react-router-dom';
import Breadcrumbs, { Breadcrumb } from '../Breadcrumbs';

const meta: Meta<typeof Breadcrumbs> = {
  title: 'Components/Breadcrumbs',
  component: Breadcrumbs,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    breadcrumbs: {
      control: 'object',
      description: 'Array of breadcrumb objects with label and optional url',
    },
  },
  decorators: [
    (Story) => (
      <MemoryRouter>
        <Story />
      </MemoryRouter>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof meta>;

// Sample breadcrumb data
const simpleBreadcrumbs: Breadcrumb[] = [
  { label: 'Startseite', url: '/' },
  { label: 'Kategorien', url: '/kategorien' },
  { label: 'Aktuelle Seite' },
];

const deepBreadcrumbs: Breadcrumb[] = [
  { label: 'Home', url: '/' },
  { label: 'Produkte', url: '/produkte' },
  { label: 'Elektronik', url: '/produkte/elektronik' },
  { label: 'Computer', url: '/produkte/elektronik/computer' },
  { label: 'Laptops', url: '/produkte/elektronik/computer/laptops' },
  { label: 'Gaming Laptops' },
];

const singleBreadcrumb: Breadcrumb[] = [
  { label: 'Startseite' },
];

const withoutHomePage: Breadcrumb[] = [
  { label: 'Dashboard', url: '/dashboard' },
  { label: 'Benutzer', url: '/dashboard/benutzer' },
  { label: 'Profil' },
];

const longLabelsBreadcrumbs: Breadcrumb[] = [
  { label: 'Sehr lange Startseite mit vielen Wörtern', url: '/' },
  { label: 'Eine sehr ausführliche Kategorienbeschreibung', url: '/kategorie' },
  { label: 'Ein unglaublich langer Seitentitel der möglicherweise umgebrochen werden muss' },
];

export const Default: Story = {
  args: {
    breadcrumbs: simpleBreadcrumbs,
  },
};

export const DeepNavigation: Story = {
  args: {
    breadcrumbs: deepBreadcrumbs,
  },
};

export const SinglePage: Story = {
  args: {
    breadcrumbs: singleBreadcrumb,
  },
};

export const WithoutHomePage: Story = {
  args: {
    breadcrumbs: withoutHomePage,
  },
};

export const LongLabels: Story = {
  args: {
    breadcrumbs: longLabelsBreadcrumbs,
  },
};

export const AllLinksClickable: Story = {
  args: {
    breadcrumbs: [
      { label: 'Startseite', url: '/' },
      { label: 'Bereich 1', url: '/bereich1' },
      { label: 'Bereich 2', url: '/bereich1/bereich2' },
      { label: 'Bereich 3', url: '/bereich1/bereich2/bereich3' },
    ],
  },
};

export const NoLinksOnly: Story = {
  args: {
    breadcrumbs: [
      { label: 'Startseite' },
      { label: 'Bereich 1' },
      { label: 'Aktuelle Seite' },
    ],
  },
};