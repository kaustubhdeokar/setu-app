import axios from "axios";
import config from "../config/config";

export const registration = async (formData) => {
  const payload = {
    username: formData.username,
    password: formData.password,
    pan_number: formData.panNumber,
  };
  const API_URL = config.apiUrl;
  console.log("Making request to:", `${API_URL}/register`);
  console.log("With payload:", payload);

  try {
    const response = await axios.post(`${API_URL}/register`, payload, {
      headers: {
        "Content-Type": "application/json",
      },
      validateStatus: false,
      timeout: 50000,
    });
    console.log("User created:", response.data.user);
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

export const login = async (formData) => {
  const payload = { username: formData.username, password: formData.password };
  const API_URL = config.apiUrl;
  console.log("Making request to:", `${API_URL}/login`);
  const base64Credentials = btoa(`${formData.username}:${formData.password}`);

  try {
    const response = await axios.post(`${API_URL}/login`, payload, {
      headers: {
        Authorization: `Basic ${base64Credentials}`,
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      validateStatus: false,
      timeout: 500000,
    });
    if (response.data.status === 200) {
      localStorage.setItem("access_token", response.data.access_token);
      localStorage.setItem("refresh_token", response.data.refresh_token);
      localStorage.setItem("user", formData.username);
    }
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

export const isUserLoggedIn = () => {
  const username = localStorage.getItem("user");
  if (username == null) {
    return false;
  } else {
    return true;
  }
};

export const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");
}

export const getAnalyticsEntries = async () => {
  const API_URL = config.apiUrl;
  const token = localStorage.getItem("token");
  try {
    const response = await axios.get(`${API_URL}/analyticsdata`, {
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
