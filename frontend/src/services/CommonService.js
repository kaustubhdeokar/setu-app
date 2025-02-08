import axios from "axios";
import config from "../frontend/src/config/config";

export const logout = () => localStorage.clear();
export const getToken = () => localStorage.getItem("token");
const API_URL = config.apiUrl;

