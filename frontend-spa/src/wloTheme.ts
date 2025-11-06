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
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 20,
          textTransform: "none",
          fontFamily: "Montserrat, sans-serif",
          fontWeight: 600,
          fontSize: "15.5px",
          padding: "2px 29px",
        },
      },
    },
  },
};
