
import { Card, CardContent, CardHeader, Divider, TextField, TextFieldProps } from '@mui/material';
// icon
import RobotIcon from "./assets/icons/robot.svg?react";

export default function MdsEditor(props: {
    title: string;
    icon?: React.ReactNode;
    children?: React.ReactNode;
}) {

    const icon = props.icon ? props.icon : <RobotIcon style={{ width: 32, height: 32 }} />;

  return (
    <Card variant='outlined'>
        {/* <CardHeader title="MDS Editor" avatar={<RobotIcon />} /> */}
        
        <div style={{ display: 'flex', alignItems: 'center', backgroundColor: '#f7f7f7', color: '#585858', 
            padding: '12px 16px', gap: 12, fontWeight: 500, textTransform: 'uppercase' }}>
          {icon}
          <span>{props.title}</span>
        </div>
        <Divider />
        <CardContent>
            {props.children}
      </CardContent>
    </Card>
  );
}