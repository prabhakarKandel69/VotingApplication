import React, { useState, useEffect } from "react";
import axios from "axios";

const VoterList = () => {
    const [voters, setVoters] = useState([]);
    const [error, setError] = useState("");

    const token = localStorage.getItem("accessToken");

    useEffect(() => {
        fetchVoters();
    }, []);

    const fetchVoters = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/voters/voters/", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setVoters(response.data);
        } catch (err) {
            setError(err.response?.data?.message || "Error fetching voters.");
        }
    };

    return (
        <div style={{ maxWidth: "600px", margin: "20px auto", padding: "20px", border: "1px solid #ccc", borderRadius: "5px" }}>
            <h2 style={{ textAlign: "center" }}>Voter List</h2>
            {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
            <ul>
                {voters.map((voter) => (
                    <li key={voter.id}>{voter.full_name} - {voter.permanent_address}</li>
                ))}
            </ul>
        </div>
    );
};

export default VoterList;
