import axios from "axios";
import config from "../config/config";

export const verifyPan = async (pan) => {
  const token = localStorage.getItem("access_token");
  const payload = {
    pan: pan,
    consent: "Y",
    reason: "Reason for verifying PAN set by the developer",
  };
  const API_URL = config.apiUrl;
  const url = `${API_URL}/api/verify/pan`;
  console.log("pan card : url: " + url);
  try {
    const response = await axios.post(url, payload, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      validateStatus: false,
      timeout: 50000,
    });
    console.log("Response received:", response);

    return response;
  } catch (error) {
    console.error("Error details:", {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      headers: error.response?.headers,
    });
    throw error;
  }
};
