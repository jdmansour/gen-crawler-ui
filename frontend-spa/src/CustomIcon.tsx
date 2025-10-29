import { AccessibilityNewOutlined, CopyrightOutlined, DescriptionOutlined, DoneAllOutlined, SchoolOutlined } from "@mui/icons-material";
import { ErrorOutlineOutlined, EditOutlined, PendingOutlined, FrontHandOutlined, SmartToyOutlined } from "@mui/icons-material";

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
