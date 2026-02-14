import { ThemeOptions } from "@mui/material";

export const wloThemeData: ThemeOptions = {
  palette: {
    mode: 'light',
    primary: {
      main: '#003b7c',
    },
    secondary: {
      main: '#ea4b71',
    },
  },
  typography: {
    h6: {
        fontFamily: "Open Sans, sans-serif",
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          variants: [
            {
              props: { variant: 'contained' },
              style: { 
                borderRadius: 20,
                textTransform: "none",
                fontFamily: "Open Sans, sans-serif",
                fontWeight: 600,
                fontSize: "15.5px",
                padding: "2px 29px",
              },
            },
            {
              props: { variant: 'outlined' },
              style: { 
                borderRadius: 20,
                textTransform: "none",
                fontFamily: "Open Sans, sans-serif",
                fontWeight: 600,
                fontSize: "15.5px",
                padding: "2px 29px",
              },
            },
            {
              props: { variant: 'text' },
              style: {
                textTransform: "none",
              },
            },
          ],
        },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: {
          borderRadius: 16,
        },
      },
    },
  },
};
