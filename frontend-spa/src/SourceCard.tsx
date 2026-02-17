import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import CardActionArea from "@mui/material/CardActionArea";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import { SourceItem } from "./apitypes";
import sourcePreviewPic from "./assets/source-preview.jpg";

export default function SourceCard(props: { sourceItem?: SourceItem }) {
  const { sourceItem } = props;
  const sourceLink = sourceItem?.data?.content?.url || null;
  return <Card sx={{ maxWidth: 345, minWidth: 250 }}>
    <CardActionArea href={sourceLink} disabled={!sourceItem}>
      <CardMedia
        sx={{ height: 140, }}
        image={sourceItem?.preview_url || sourcePreviewPic}
        title="Vorschau" />
      <CardContent>
        {sourceItem && (
          <Typography gutterBottom variant="h5" component="div">
            {sourceItem.title}
          </Typography>)}
        <Typography variant="body2" sx={{ color: 'text.secondary' }}>
          {sourceItem ? sourceItem.description : "Keine Quelle ausgewählt"}
        </Typography>
      </CardContent>
    </CardActionArea>
    <CardActions sx={{ display: 'flex', justifyContent: 'flex-end' }}>
      {sourceItem ? <>
        <Button size="small" disabled>Quelle ändern</Button>
        <Button size="small" href={sourceLink}>Details</Button>
      </> :
        <Button size="small" disabled>Quelle auswählen</Button>}
    </CardActions>
  </Card>;
}