import process from "process"

const config = {
    apiUrl: import.meta.env.VITE_API_URL,
    environment: import.meta.env.VITE_ENV,
    featureFlags: {
        newFeature: process.env.VITE_ENV === 'development',
    },
};

export default config;  