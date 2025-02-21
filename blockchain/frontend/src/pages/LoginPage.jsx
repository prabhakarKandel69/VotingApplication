import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios"; // Ensure axios is installed and imported
import useWallet from "../hooks/useWallet";

const LoginPage = () => {
  const [phone, setPhone] = useState(""); // For phone number
  const [password, setPassword] = useState(""); // For password
  const [message, setMessage] = useState(""); // For error or success message
  const navigate = useNavigate();
  const { signer } = useWallet();

  // Handle login
  const handleLogin = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior

    // Validate phone number using regex (e.g., for Indian phone numbers)
    const phoneRegex = /^[6-9]\d{9}$/;
    if (!phoneRegex.test(phone)) {
      setMessage("Please enter a valid 10-digit phone number.");
      return;
    }

    try {
      // Send a POST request to the backend with phone number and password
      const response = await axios.post("http://127.0.0.1:8000/user/login/", {
        phone,
        password,
      });

      // Check if the response contains the tokens
      const { access, refresh, admin } = response.data;

      if (access && refresh) {
        // Store tokens securely in localStorage
        localStorage.setItem("accessToken", access);
        localStorage.setItem("refreshToken", refresh);
        localStorage.setItem('admin', admin)
        setMessage("Login successful!");

        // Redirect the user to the dashboard page
        navigate("/dashboard");
      } else {
        // If tokens are missing in the response, display a failure message
        setMessage("Login failed. Tokens are missing.");
      }
    } catch (error) {
      // Handle errors
      if (error.response) {
        // If the backend returns an error message
        setMessage(error.response.data.detail || "Login failed.");
      } else {
        // If a network error or other issue occurs
        setMessage("An error occurred. Please try again.");
      }
    }
  };

  return (
    <div className="login-page">
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        <div>
          <label>Phone</label>
          <input
            type="text"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="Enter your phone number"
            required
          />
        </div>
        <div>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
          />
        </div>
        {message && <p style={{ color: "red" }}>{message}</p>}
        <button type="submit">Login</button>
        <button type="button" onClick={() => navigate("/")}>
          Back to Home
        </button>
      </form>
      <p>
        Don't have an account? <a href="/new-registration">Register here</a>
      </p>
    </div>
  );
};

export default LoginPage;
