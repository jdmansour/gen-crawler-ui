
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Divider from '@mui/material/Divider';
import RobotIcon from "./assets/icons/robot.svg?react";

export default function MdsEditor(props: {
    title: string | React.ReactNode;
    icon?: React.ReactNode;
    children?: React.ReactNode;
}) {

    const icon = props.icon ? props.icon : <RobotIcon style={{ width: 32, height: 32 }} />;

  return (
    <Card variant='outlined'>
        <div style={{ display: 'flex', alignItems: 'center', backgroundColor: '#f7f7f7', color: '#585858', 
            padding: '12px 16px', gap: 12, fontWeight: 500, textTransform: 'uppercase' }}>
          {icon}
          {typeof props.title === 'string' ? <span>{props.title}</span> : props.title}
        </div>
        <Divider />
        <CardContent>
            {props.children}
      </CardContent>
    </Card>
  );
}