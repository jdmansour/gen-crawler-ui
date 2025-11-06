import AccessibilityNewOutlined from '@mui/icons-material/AccessibilityNewOutlined';
import CopyrightOutlined from '@mui/icons-material/CopyrightOutlined';
import DescriptionOutlined from '@mui/icons-material/DescriptionOutlined';
import DoneAllOutlined from '@mui/icons-material/DoneAllOutlined';
import EditOutlined from '@mui/icons-material/EditOutlined';
import ErrorOutlineOutlined from '@mui/icons-material/ErrorOutlineOutlined';
import FrontHandOutlined from '@mui/icons-material/FrontHandOutlined';
import PendingOutlined from '@mui/icons-material/PendingOutlined';
import SchoolOutlined from '@mui/icons-material/SchoolOutlined';
import SmartToyOutlined from '@mui/icons-material/SmartToyOutlined';

export function CustomIcon(props: { iconName: string|undefined; }) {
    switch (props.iconName) {
        case "description":
            return <DescriptionOutlined />;
        case "school":
            return <SchoolOutlined />;
        case "done_all":
            return <DoneAllOutlined />;
        case "copyright":
            return <CopyrightOutlined />;
        case "accessibility":
            return <AccessibilityNewOutlined />;
        case "robot":
            return <SmartToyOutlined />;
        case "error":
            return <ErrorOutlineOutlined />;
        case "edit":
            return <EditOutlined />;
        case "pending":
            return <PendingOutlined />;
        case "stop":
            return <FrontHandOutlined />;
        default:
            return <></>;
    }
}
