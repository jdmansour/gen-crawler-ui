import { ThemeOptions } from "@mui/material";
import { createTheme } from "@mui/material/styles";

const baseTheme = createTheme({
  typography: {
    fontFamily: "Open Sans, sans-serif",
    fontSize: 14,
  },
});

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
    fontFamily: "Open Sans, sans-serif",
    fontSize: baseTheme.typography.fontSize,
    // fontSize: 12,
    "h3": {
      fontFamily: "Montserrat, sans-serif",
      fontSize: baseTheme.typography.pxToRem(19.2),
      fontWeight: 600,
    },
    "h5": {
      fontFamily: "Montserrat, sans-serif",
      fontSize: baseTheme.typography.pxToRem(16),
      fontWeight: 600,
    },
    // "h6": {
    //   fontFamily: "Montserrat, sans-serif",
    //   fontWeight: 700,
    // },
    button: {
      fontFamily: "Montserrat, sans-serif",
      // fontSize: baseTheme.typography.pxToRem(14),
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
                // fontFamily: "Montserrat, sans-serif",
                fontWeight: 600,
                // fontSize: "15.5px",
                // padding: "2px 29px 2px",
                // padding: "0.1em 1em 0.1em",
              },
            },
            {
              props: { variant: 'outlined' },
              style: { 
                borderRadius: 20,
                textTransform: "none",
                // fontFamily: "Montserrat, sans-serif",
                fontWeight: 600,
                // fontSize: "15.5px",
                // // fontSize: "1em",
                // padding: "2px 29px 2px",
                // padding: "0.1em 1em 0.1em",
                // boxShadow: `0px 0px 4px 1px ${baseTheme.palette.primary.main} inset`,
              },
            },
            {
              props: { variant: 'text' },
              style: {
                // fontFamily: "Montserrat, sans-serif",
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
    MuiChip: {
      styleOverrides: {
        root: {
          // fontFamily: "Montserrat, sans-serif",
          // borderRadius: 8,
        },
      },
    },
  },
};
