import { createContext, useContext } from "react";

// Context for base API URL
export const SidebarComponentContext = createContext<{apiUrl?: string, basePath?: string}>({});

// Hook for components to access it
export const useSidebarComponentContext = () => {
    const {apiUrl = 'http://localhost:8000/api', basePath = ""} = useContext(SidebarComponentContext);
    return {apiUrl, basePath}
};
