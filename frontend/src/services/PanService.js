import axios from "axios";
import config from "../config/config";


export const verifyPan = async (pan) => {
    const payload = {pan: pan, consent: "Y", reason:"Reason for verifying PAN set by the developer"};
    const API_URL = config.apiUrl;
    try{
        const response = await axios.post(`${API_URL}/api/verify/pan`, payload, {
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
