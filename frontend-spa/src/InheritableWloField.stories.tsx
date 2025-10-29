import type { Meta, StoryObj } from '@storybook/react-vite';
import InheritableWloField from './InheritableWloField';

const meta = {
  component: InheritableWloField,
  tags: ['autodocs'],
} satisfies Meta<typeof InheritableWloField>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Text: Story = {
  args: {
    field: {
      "id": "cclom:title",
      "type": "text",
      "inheritable": true,
      "recommended": true,
      "caption": "Voller Titel",
      "bottomCaption": "Name des Inhalts",
      "placeholder": "Gib dem Inhalt einen Namen",
      "value": "Klexikon (Quellen-Datensatz Testobjekt)"
    },
  }
};

export const TextNotRecommended: Story = {
  args: {
    field: {
      "id": "cclom:title",
      "type": "text",
      "inheritable": true,
      "recommended": false,
      "caption": "Voller Titel",
      "bottomCaption": "Name des Inhalts",
      "placeholder": "Gib dem Inhalt einen Namen",
      "value": "Klexikon (Quellen-Datensatz Testobjekt)"
    },
  }
};

export const TextNotInheritable: Story = {
  args: {
    field: {
      "id": "cclom:title",
      "type": "text",
      "inheritable": false,
      "recommended": false,
      "caption": "Voller Titel",
      "bottomCaption": "Name des Inhalts",
      "placeholder": "Gib dem Inhalt einen Namen",
      "value": "Klexikon (Quellen-Datensatz Testobjekt)"
    },
  }
};

export const Textarea: Story = {
  args: {

    field: {
      "id": "cclom:general_description",
      "inheritable": true,
      "recommended": true,
      "type": "textarea",
      "caption": "Beschreibung",
      "bottomCaption": "Beschreibe den Inhalt",
      "placeholder": "Das MATERIALART des ANBIETERS zeigt INHALTSBESCHREIBUNG. Es eignet sich für ZWECK für folgende ZIELGRUPPE",
      "value": "Das freie Internet-Lexikon Klexikon ist ein Wiki mit kindgerechten Inhalten und Ansprache für die Altersgruppe von etwa 6-12 Jahren.\n\n(TestObjekt - Kopie des Quellen-Datensatzes auf Prod: https://redaktion.openeduhub.net/edu-sharing/components/render/0a504542-b202-4835-9b64-196c99814226 )"
    },

    selected: true
  }
};

export const MultivalueFixedBadges: Story = {
  args: {
    field: {
      "id": "cclom:general_language",
      "type": "multivalueFixedBadges",
      "inheritable": true,
      "recommended": true,
      "caption": "Sprache(n)",
      "bottomCaption": "Alle Sprachen, die im Dokument vorkommen",
      "placeholder": null,
      "values": [
        {
          "value": "de_DE",
          "display": "Deutsch (Deutschland)"
        },
        {
          "value": "en_US",
          "display": "Englisch (Vereinigte Staaten)"
        }
      ]
    },
  }
};