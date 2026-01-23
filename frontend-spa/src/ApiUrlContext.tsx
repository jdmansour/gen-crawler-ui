import { createContext, useContext } from "react";

// Context for base API URL
export const ApiUrlContext = createContext<string | null>(null);

// Hook for components to access it
export const useApiUrl = () => {
    const context = useContext(ApiUrlContext);
    if (!context) {
        return 'http://localhost:8000/api';
    }
    return context;
};
