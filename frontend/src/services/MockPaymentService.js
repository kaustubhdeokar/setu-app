import axios from "axios";
import config from "../config/config";

export const makePaymentRequest = async () => 
{
    const token = localStorage.getItem('token'); 
    const API_URL = config.apiUrl;
    try{
        const response = await axios.post(`${API_URL}/api/verify/ban/reverse`, {}, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
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

export const fetchBankDetails = async (request_id) => {
    const token = localStorage.getItem('token'); 
    const API_URL = config.apiUrl;
    try{
        const response = await axios.get(`${API_URL}/api/verify/ban/reverse/`+request_id, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            validateStatus: false,
            timeout: 30000,
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

export const updateAnalytics = async (username) => {
    const token = localStorage.getItem('token'); 
    const API_URL = config.apiUrl;
    console.log('update analytics triggered.')
    try{
        const response = await axios.get(`${API_URL}/update-analytics/`+username, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            validateStatus: false,
            timeout: 30000,
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