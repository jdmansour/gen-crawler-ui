import AddIcon from '@mui/icons-material/Add';
import MoreVertOutlined from "@mui/icons-material/MoreVertOutlined";
import { ButtonBase } from '@mui/material';
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";
import { createTheme } from "@mui/material/styles";
import Typography from "@mui/material/Typography";
import ThemeProvider from "@mui/system/ThemeProvider";
import { Robot } from "@nine-thirty-five/material-symbols-react/outlined";
import { DateTime } from "luxon";
import { Crawler, SourceItem } from "./apitypes";
import { wloThemeData } from "./wloTheme";
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
  basePath?: string;
}

export default function SourceDetailsSidebar(props: SourceDetailsSidebarProps) {
  const { crawlers, basePath="" } = props;
  const wloTheme = createTheme(wloThemeData);

  console.log("In SourceDetailsSidebar, basePath:", basePath);
  const addCrawlerForSourcePath = joinPath(basePath, `add-crawler?sourceGuid=${props.sourceItem?.guid}`);

  return (
    <Stack spacing={2} sx={{ p: 2 }}>
      {/* <SourceCard sourceItem={sourceItem} orientation="horizontal" /> */}

      {/* <Typography variant="h6">Crawler</Typography> */}
      {/* <ThemeProvider  theme={roundedTheme}> */}

      <ThemeProvider theme={wloTheme}>

      <Typography variant="body2">Bereits existierende Crawler zu dieser Quelle:</Typography>

      <Box sx={{ display: "flex", flexDirection: "column", gap: "1px" }}>
        {crawlers && crawlers.length > 0 ? (
          crawlers.map(crawler => (
            <ButtonBase
              key={crawler.id}
              sx={{
                display: "flex",
                width: "100%",
                alignItems: "center",
                justifyContent: "stretch",
                borderRadius: "12px",
                overflow: "hidden",
                backgroundColor: "background.paper",
                boxShadow: 2,
                gap: 2,
                px: 2,
                py: 1,
                fontSize: "0.875rem",
                "&:hover": { backgroundColor: "#efefef" },
                // "& > *": { outline: "1px solid orange" },
                // "& > * > *": { outline: "1px solid blue" },
              }}
              component={"a"}
              href={joinPath(basePath, `crawlers/${crawler.id}`)}
              // if the click is on the more button, do not navigate
              onClick={(e) => {
                if ((e.target as HTMLElement).closest("button")) {
                  e.preventDefault();
                }
              }}
              onPointerDown={e => { if (e.pointerType === "mouse" && e.button === 2) e.preventDefault(); }}
            >
              <Box sx={{ pt: "3px", pl: "2px" }}><Robot /></Box>
              <Box style={{ textAlign: "left", flex: 1 }}>
                <Typography variant="subtitle2">{crawler.name}</Typography>
              </Box>
              <Box sx={{ color: "text.secondary" }}>
                <Typography variant="caption" >
                {DateTime.fromISO(crawler.updated_at).toRelative({style: "short"})}
                </Typography>
              </Box>
              <Box sx={{ m: -1, ml: -2 }}>
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
          <Button variant="contained" color="primary" component={"a"} href={addCrawlerForSourcePath}>
            <AddIcon sx={{ mr: 1, ml: -1 }} />
            Crawler hinzufügen
          </Button>
        </Stack>
      </ThemeProvider>


    </Stack>
  );
}

// joinPath("base/", "/add-crawler") => "base/add-crawler"
// joinPath("", "add-crawler") => "add-crawler"
// joinPath("/", "/add-crawler") => "/add-crawler"
function joinPath(...parts: string[]) {
  return parts.map((part, index) => {
    if (index === 0) {
      return part.replace(/\/+$/, ""); // remove trailing slashes from the first part
    } else {
      return part.replace(/^\/+/, ""); // remove leading slashes from subsequent parts
    }
  }).filter(part => part.length > 0).join("/");
}