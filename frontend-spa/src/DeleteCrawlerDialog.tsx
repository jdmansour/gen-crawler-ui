import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";

export default function DeleteCrawlerDialog(props: {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
}) {
  return (
    <Dialog
      open={props.open}
      onClose={props.onClose}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle id="alert-dialog-title">
        {"Crawler wirklich löschen?"}
      </DialogTitle>
      <DialogContent>
        <DialogContentText id="alert-dialog-description">
          Diese Aktion kann nicht rückgängig gemacht werden. Alle zugehörigen Crawls werden ebenfalls gelöscht.
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={props.onClose} autoFocus>Abbrechen</Button>
        <Button onClick={props.onConfirm} color="error">Löschen</Button>
      </DialogActions>
    </Dialog>
  );
}