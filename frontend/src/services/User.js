import axios from "axios";
import config from "../config/config";


export const registration = async (formData) => {
    
    const payload = {username: formData.username, password: formData.password, pan_number: formData.panNumber};
    const API_URL = config.apiUrl;

    try{
        const response = await axios.post(`${API_URL}/register`, payload, {
            headers: {
                'Content-Type': 'application/json',
            },
            validateStatus: false,
            timeout: 50000,
        });
        console.log('Response received:', response);
        return response;
    }
    catch (error) {
        console.error('Error details:', {
            message: error.message,
            response: error.response?.data,
            status: error.response?.status,
            headers: error.response?.headers
        });
        throw error;
    }
}

export const login = async (formData) => {
    const payload = {username: formData.username, password: formData.password};
    const API_URL = config.apiUrl;
    console.log(JSON.stringify(payload));

    const base64Credentials = btoa(`${formData.username}:${formData.password}`);

    try{
        const response = await axios.post(`${API_URL}/login`, payload, {
            headers: {
                'Authorization': `Basic ${base64Credentials}`,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            validateStatus: false,
            timeout: 50000,
        });
        return response;
    }
    catch (error) {
        console.error('Error details:', {
            message: error.message,
            response: error.response?.data,
            status: error.response?.status,
            headers: error.response?.headers
        });
        throw error;
    }
}