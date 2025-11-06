import Add from '@mui/icons-material/Add';
import AppsRounded from '@mui/icons-material/AppsRounded';
import FilterList from '@mui/icons-material/FilterList';
import KeyboardArrowDown from "@mui/icons-material/KeyboardArrowDown";
import Menu from '@mui/icons-material/Menu';
import Search from '@mui/icons-material/Search';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import { deepOrange } from "@mui/material/colors";
import IconButton from "@mui/material/IconButton";
import InputAdornment from '@mui/material/InputAdornment';
import TextField from '@mui/material/TextField';
import { Stack } from "@mui/system";
import { useNavigate } from "react-router";

export default function WloFakeHeader() {
  const navigate = useNavigate();
  return <div>
    <Stack direction="row" alignItems="center" spacing={1} sx={{ pr: 3 }}>
      <Button sx={{ pl: 2.25, pt: 3.75, pb: 4, borderRadius: 0 }} onClick={() => navigate("/")}>
        <Stack direction="row" alignItems="center" spacing={1.9}>
          <Menu />
          <img src="https://repository.staging.openeduhub.net/edu-sharing/assets/images/wlo-short.svg" alt="WLO Logo" style={{ height: 40 }} />
        </Stack>
      </Button>
      <Button variant="contained" sx={{
        backgroundColor: '#e4f700',
        color: '#003b7c',
        fontSize: 18,
        boxShadow: 'none',
        '&:hover': {
          backgroundColor: '#d4e600',
          boxShadow: 'none',
        },
        borderRadius: 15,
        textTransform: 'none',
      }} startIcon={<Add />}>
        Neu
      </Button>
      <TextField variant="outlined"
        sx={{ flexGrow: 1, maxWidth: 600 }}
        style={{ marginInline: 'auto' }}
        slotProps={{
          input: {
            sx: { borderRadius: 15, fontSize: 13 },
            // style: { paddingTop: 1, paddingBottom: 8 },
            startAdornment: (
              <InputAdornment position="start">
                <IconButton><Search /></IconButton>
                <IconButton><FilterList /></IconButton>
              </InputAdornment>
            ),
          },
          htmlInput: {
            sx: { pt: 1.5, pb: 1.5 },
          }
        }}
        placeholder="Suchen in Inhalte-Buffets... (fake)" />
      <IconButton>
        <AppsRounded sx={{ fontSize: 24 }} />
      </IconButton>

      <IconButton sx={{ borderRadius: 15 }}>
        {/* <AccountCircle sx={{ fontSize: 24 }} /> */}
        <Avatar sx={{ bgcolor: deepOrange[500], width: 24, height: 24, fontSize: 11 }}>JM</Avatar>
        <KeyboardArrowDown />
      </IconButton>
    </Stack>
  </div>;
}
