import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import CardActionArea from "@mui/material/CardActionArea";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import { SourceItem } from "./apitypes";
import sourcePreviewPic from "./assets/source-preview.jpg";
import { Stack } from "@mui/material";

export default function SourceCard(props: { sourceItem?: SourceItem, orientation?: "horizontal" | "vertical" }) {
  const { sourceItem } = props;
  const sourceLink = sourceItem?.data?.content?.url || null;
  if (props.orientation === "horizontal") {
    return <Card sx={{ maxWidth: 600, maxHeight: 220, flexBasis: 500, display: 'flex', flexShrink: 1, flexGrow: 1, flexDirection: 'row', alignItems: 'stretch', gap: 0 }}>
      <CardMedia
        sx={{ minWidth: 200, flexGrow: 0 }}
        image={sourceItem?.preview_url || sourcePreviewPic}
        title="Vorschau" />
      <Stack sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <CardActionArea href={sourceLink} disabled={!sourceItem} sx={{ pl: 3, pr: 2, pt: 2, pb: 2, height: '100%' }}>
          {sourceItem && (
            <Typography gutterBottom variant="h5" component="div">
              {sourceItem.title}
            </Typography>)}
          <Typography variant="body2" sx={{ color: 'text.secondary', maxHeight: 60, overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {sourceItem ? sourceItem.description : "Keine Quelle ausgewählt"}
          </Typography>
        </CardActionArea>
        <CardActions sx={{ display: 'flex', justifyContent: 'flex-end' }}>
          {sourceItem ? <>
            <Button size="small" disabled>Quelle ändern</Button>
            <Button size="small" href={sourceLink}>Details</Button>
          </> :
            <Button size="small" disabled>Quelle auswählen</Button>}
        </CardActions>
      </Stack>

    </Card>;
  }

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


// export default function SourceCard(props: { sourceItem?: SourceItem }) {
//   const { sourceItem } = props;
//   const sourceLink = sourceItem?.data?.content?.url || null;
//   return <Card sx={{ maxWidth: 345, minWidth: 250 }}>
//     <CardActionArea href={sourceLink} disabled={!sourceItem}>
//       <CardMedia
//         sx={{ height: 140, }}
//         image={sourceItem?.preview_url || sourcePreviewPic}
//         title="Vorschau" />
//       <CardContent>
//         {sourceItem && (
//           <Typography gutterBottom variant="h5" component="div">
//             {sourceItem.title}
//           </Typography>)}
//         <Typography variant="body2" sx={{ color: 'text.secondary' }}>
//           {sourceItem ? sourceItem.description : "Keine Quelle ausgewählt"}
//         </Typography>
//       </CardContent>
//     </CardActionArea>
//     <CardActions sx={{ display: 'flex', justifyContent: 'flex-end' }}>
//       {sourceItem ? <>
//         <Button size="small" disabled>Quelle ändern</Button>
//         <Button size="small" href={sourceLink}>Details</Button>
//       </> :
//         <Button size="small" disabled>Quelle auswählen</Button>}
//     </CardActions>
//   </Card>;
// }