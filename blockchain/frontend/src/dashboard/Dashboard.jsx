import React, { useState, useEffect } from "react";
import axios from "axios";
import "./dashboard.css";
import AddCandidate from "../pages/AddCandidate";
import VoterList from "../pages/VoterList";
import { ethers } from "ethers";

function Dashboard() {
    const [candidates, setCandidates] = useState([]);
    const [formData, setFormData] = useState({
        full_name: "",
        middle_name: "",
        last_name: "",
        permanent_address: "",
        temporary_address: "",
        age: "",
        dob: "",
        blood_group: "",
    });
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [voterExists, setVoterExists] = useState(false);
    const [userAccount, setUserAccount] = useState(null);
    const [loading, setLoading] = useState(false);

    const token = localStorage.getItem("accessToken");
    const isAdmin = localStorage.getItem("admin") === "true";

    useEffect(() => {
        fetchCandidates();
        checkVoterStatus();
    }, []);

    // Fetch candidates from the backend
    const fetchCandidates = async () => {
        setLoading(true);
        setError("");
        try {
            const response = await axios.get("http://127.0.0.1:8000/candidate/candidates/", {
                headers: { Authorization: `Bearer ${token}` },
            });
            if (response.data && Array.isArray(response.data)) {
                setCandidates(response.data);
                console.log(response.data);

            } else {
                setError("Invalid candidates data format from the server.");
            }
        } catch (err) {
            console.error("Error fetching candidates:", err);
            setError(err.response?.data?.message || "Failed to fetch candidates.");
        } finally {
            setLoading(false);
        }
    };

    // Check voter registration status
    const checkVoterStatus = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/voters/voters/user/", {
                headers: { Authorization: `Bearer ${token}` },
            });

            if (Array.isArray(response.data)) {
                setVoterExists(response.data.length > 0);
            } else {
                setError("Invalid response format from server.");
            }
        } catch (err) {
            setError(err.response?.data?.message || "Error checking voter status.");
        }
    };

    // Handle voting
    const handleVote = async (candidateId) => {
        if (!userAccount) {
            alert("Please connect MetaMask first.");
            return;
        }

        if (!token) {
            setError("Authorization token is missing.");
            return;
        }

        setError("");
        setSuccess("");
        setLoading(true);

        try {
            let data = new FormData();
            data.append("candidate", candidateId);

            const response = await axios.post(
                `http://127.0.0.1:8000/votes/votes/`,
                data, // Pass the data as the second argument
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );

            if (response.data && response.data.success) {
                setSuccess("Your vote has been successfully cast!");
                fetchCandidates(); // Refresh candidates to update vote count
                return;
            }

        } catch (err) {
            console.error("Error casting vote:", err);
            setError(err.response?.data?.message || "Error casting vote.");
        } finally {
            setLoading(false);
        }
    };


    // Handle form input changes for voter registration
    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value.trim() });
    };

    // Add new voter
    const handleAddVoter = async (e) => {
        e.preventDefault();

        const requiredFields = ["full_name", "last_name", "permanent_address", "age", "dob"];
        for (const field of requiredFields) {
            if (!formData[field] || formData[field].trim() === "") {
                setError(`Please fill in the required field: ${field.replace("_", " ")}`);
                return;
            }
        }

        if (isNaN(formData.age) || formData.age <= 0) {
            setError("Age must be a valid number greater than 0.");
            return;
        }

        if (new Date(formData.dob) > new Date()) {
            setError("Date of birth must be in the past.");
            return;
        }

        setLoading(true);
        try {
            await axios.post("http://127.0.0.1:8000/voters/voters/create/", formData, {
                headers: { Authorization: `Bearer ${token}` },
            });

            setVoterExists(true);
            setFormData({
                full_name: "",
                middle_name: "",
                last_name: "",
                permanent_address: "",
                temporary_address: "",
                age: "",
                dob: "",
                blood_group: "",
            });
            setSuccess("Voter registered successfully!");
        } catch (err) {
            setError(err.response?.data?.message || "Error registering voter.");
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.clear();
        window.location.href = "/";
    };

    const connectMetaMask = async () => {
        if (typeof window.ethereum !== "undefined") {
            try {
                const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
                setUserAccount(accounts[0]);
            } catch (error) {
                setError("Failed to connect MetaMask.");
            }
        } else {
            alert("Please install MetaMask.");
        }
    };

    return (
        <div className="dashboard">
            <div className="voting-section">
                <h2>Election Voting</h2>
                {loading && <p>Loading...</p>}
                {voterExists ? (
                    <div>
                        <button onClick={connectMetaMask}>Connect MetaMask</button>
                        {userAccount && <p>Connected Account: {userAccount}</p>}
                        <ul>
                            {candidates.length > 0 ? (
                                candidates.map((candidate) => (
                                    <li key={candidate.candidate_id}>
                                        <p>{candidate.full_name}</p>
                                        <p>Votes: {candidate.party}</p>
                                        <button onClick={() => handleVote(candidate.candidate_id)}>Vote</button>
                                    </li>
                                ))
                            ) : (
                                <p>No candidates available.</p>
                            )}
                        </ul>
                    </div>
                ) : (
                    <form onSubmit={handleAddVoter}>
                        <input
                            type="text"
                            name="full_name"
                            placeholder="Full Name"
                            onChange={handleInputChange}
                            value={formData.full_name}
                            required
                        />
                        <input
                            type="text"
                            name="last_name"
                            placeholder="Last Name"
                            onChange={handleInputChange}
                            value={formData.last_name}
                            required
                        />
                        <input
                            type="text"
                            name="permanent_address"
                            placeholder="Permanent Address"
                            onChange={handleInputChange}
                            value={formData.permanent_address}
                            required
                        />
                        <input
                            type="number"
                            name="age"
                            placeholder="Age"
                            onChange={handleInputChange}
                            value={formData.age}
                            required
                        />
                        <input
                            type="date"
                            name="dob"
                            onChange={handleInputChange}
                            value={formData.dob}
                            required
                        />
                        <button type="submit">Register Voter</button>
                    </form>
                )}
                {error && <p className="error">{error}</p>}
                {success && <p className="success">{success}</p>}
            </div>
            {isAdmin && (
                <div>
                    <AddCandidate />
                    <VoterList />
                </div>
            )}
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
}

export default Dashboard;
