import axios from "axios";
import { API_URL } from "./src/constant";

const axiosInstance = axios.create({
  baseURL: `${API_URL}/user`, // Django backend URL
});

export default axiosInstance;
