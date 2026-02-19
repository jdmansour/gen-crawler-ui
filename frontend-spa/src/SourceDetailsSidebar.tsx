import AddIcon from '@mui/icons-material/Add';
import MoreVertOutlined from "@mui/icons-material/MoreVertOutlined";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import { createTheme } from "@mui/material/styles";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableRow from "@mui/material/TableRow";
import Typography from "@mui/material/Typography";
import ThemeProvider from "@mui/system/ThemeProvider";
import { DateTime } from "luxon";
import { Link } from "react-router-dom";
import { Crawler, SourceItem } from "./apitypes";
import SourceCard from "./SourceCard";
import { roundedTheme } from "./TableTest";
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

      <ThemeProvider theme={roundedTheme}>
        <TableContainer component={Paper}>
          <Table size="small">
            <TableBody>
              {crawlers && crawlers.length > 0 ? (
                crawlers.map(crawler => (
                  // <TableRow key={crawler.id}>
                  <ButtonBase
                    component={TableRow} key={crawler.id}
                    sx={{
                      display: "table-row",
                      "&:hover:after": { backgroundColor: "#f5f5f5" },
                      "& .MuiTouchRipple-root": { borderRadius: 3 }
                    }}
                    onPointerDown={e => { if (e.pointerType == "mouse" && e.button === 2) { e.preventDefault(); } }}>
                    <TableCell width="100%">
                      <Link to={`/crawlers/${crawler.id}`} style={{ textDecoration: "none", color: "inherit", fontWeight: 600, display: "flex", alignItems: "center", gap: 8 }} onClick={(e) => e.stopPropagation()}>
                        <Robot style={{ color: "text.secondary" }} />
                        {/* <AddIcon sx={{ mr: 1, ml: -1 }} /> */}
                        {crawler.name}
                      </Link>
                    </TableCell>
                    {/* <TableCell>
                      <Chip
                        label={simpleStateLabels[crawler.simple_state]}
                        color={simpleStateColors[crawler.simple_state]}
                        size="small"
                      />
                    </TableCell>
                    <TableCell sx={{ maxWidth: 180, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      {crawler.start_url}
                    </TableCell> */}
                    <TableCell sx={{ whiteSpace: "nowrap", color: "text.secondary" }}>
                      {DateTime.fromISO(crawler.updated_at).toRelative()}
                    </TableCell>
                    <TableCell align="right">
                      <IconButton sx={{ mr: -1 }}
                        onMouseDown={(e) => { e.stopPropagation(); }}>
                        <MoreVertOutlined fontSize="medium" />
                      </IconButton>
                    </TableCell>
                    {/* </TableRow> */}
                  </ButtonBase>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={4} align="center" sx={{ color: "text.secondary" }}>
                    Keine Crawler für diese Quelle
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </ThemeProvider>

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
