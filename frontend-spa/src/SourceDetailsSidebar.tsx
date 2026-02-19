import AddIcon from '@mui/icons-material/Add';
import MoreVertOutlined from "@mui/icons-material/MoreVertOutlined";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";
import { createTheme } from "@mui/material/styles";
import Typography from "@mui/material/Typography";
import ThemeProvider from "@mui/system/ThemeProvider";
import { DateTime } from "luxon";
import { Link } from "react-router-dom";
import { Crawler, SourceItem } from "./apitypes";
import SourceCard from "./SourceCard";
import { wloThemeData } from "./wloTheme";
import { Robot } from "@nine-thirty-five/material-symbols-react/outlined";
import { ButtonBase, Card, CardActionArea, CardContent } from '@mui/material';
//import { RobotIcon } from "@mui/icons-material/RobotIco";

// const simpleStateLabels: { [key in SimpleState]: string } = {
//   draft: "Entwurf",
//   running: "Läuft",
//   idle: "Bereit",
//   error: "Fehler",
// };

// const simpleStateColors: { [key in SimpleState]: "default" | "primary" | "success" | "error" } = {
//   draft: "default",
//   running: "primary",
//   idle: "success",
//   error: "error",
// };

interface SourceDetailsSidebarProps {
  sourceItem?: SourceItem;
  crawlers?: Crawler[];
}

export default function SourceDetailsSidebar(props: SourceDetailsSidebarProps) {
  const { crawlers } = props;
  const wloTheme = createTheme(wloThemeData);

  return (
    <Stack spacing={2} sx={{ p: 2 }}>
      {/* <SourceCard sourceItem={sourceItem} orientation="horizontal" /> */}

      {/* <Typography variant="h6">Crawler</Typography> */}
      {/* <ThemeProvider  theme={roundedTheme}> */}

      <ThemeProvider theme={wloTheme}>

      <Typography variant="body2">Bereits existierende Crawler zu dieser Quelle:</Typography>

      <Box sx={{ display: "flex", flexDirection: "column", gap: "1px", p: "5px" }}>
        {crawlers && crawlers.length > 0 ? (
          crawlers.map(crawler => (
            <ButtonBase
              key={crawler.id}
              sx={{
                display: "grid",
                gridTemplateColumns: "1fr auto auto",
                width: "100%",
                alignItems: "center",
                borderRadius: "12px",
                overflow: "hidden",
                backgroundColor: "background.paper",
                boxShadow: 2,
                fontSize: "0.875rem",
                "&:hover": { backgroundColor: "#efefef" },
              }}
              onPointerDown={e => { if (e.pointerType === "mouse" && e.button === 2) e.preventDefault(); }}
            >
              <Box sx={{ px: 2, py: "6px" }}>
                <Link to={`/crawlers/${crawler.id}`} style={{ textDecoration: "none", color: "inherit", fontWeight: 600, display: "flex", alignItems: "center", gap: 10 }} onClick={(e) => e.stopPropagation()}>
                  <Robot style={{ color: "text.secondary" }} />
                  {crawler.name}
                </Link>
              </Box>
              <Box sx={{ px: 2, py: "6px", whiteSpace: "nowrap", color: "text.secondary" }}>
                {DateTime.fromISO(crawler.updated_at).toRelative()}
              </Box>
              <Box sx={{ py: "6px", pr: 1 }}>
                <IconButton onMouseDown={(e) => e.stopPropagation()}>
                  <MoreVertOutlined fontSize="medium" />
                </IconButton>
              </Box>
            </ButtonBase>
          ))
        ) : (
          <Box sx={{ py: 2, textAlign: "center", color: "text.secondary", fontSize: "0.875rem" }}>
            Keine Crawler für diese Quelle
          </Box>
        )}
      </Box>

      {/* Button bar */}
        <Stack direction="row" spacing={1} justifyContent="flex-end">
          <Button variant="contained" color="primary">
            <AddIcon sx={{ mr: 1, ml: -1 }} />
            Crawler hinzufügen
          </Button>
        </Stack>
      </ThemeProvider>


    </Stack>
  );
}
