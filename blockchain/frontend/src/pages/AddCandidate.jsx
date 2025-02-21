import React, { useState } from "react";
import axios from "axios";

const AddCandidate = () => {
    const [formData, setFormData] = useState({
        full_name: "",
        last_name: "",
        party: "",
        position: ""
    });
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const token = localStorage.getItem('accessToken')

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage("");
        if (!token) {
            setMessage('token not available')
            setLoading(false)
            return
        }
        const form = new FormData();
        Object.keys(formData).forEach(key => form.append(key, formData[key]));

        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/candidate/candidates/",
                form,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            setMessage("Candidate added successfully!");
            setFormData({ full_name: "", last_name: "", party: "", position: "" });
        } catch (error) {
            setMessage("Error adding candidate");
            console.error(error);
        }
        setLoading(false);
    };

    return (
        <div style={{ maxWidth: "400px", margin: "20px auto", padding: "20px", border: "1px solid #ccc", borderRadius: "5px" }}>
            <h2 style={{ textAlign: "center" }}>Add Candidate</h2>
            {message && <p style={{ color: "gray", textAlign: "center" }}>{message}</p>}
            <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                <input name="full_name" value={formData.full_name} onChange={handleChange} placeholder="Full Name" required style={{ padding: "8px", border: "1px solid #ccc", borderRadius: "4px" }} />
                <input name="last_name" value={formData.last_name} onChange={handleChange} placeholder="Last Name" required style={{ padding: "8px", border: "1px solid #ccc", borderRadius: "4px" }} />
                <input name="party" value={formData.party} onChange={handleChange} placeholder="Party" required style={{ padding: "8px", border: "1px solid #ccc", borderRadius: "4px" }} />
                <input name="position" value={formData.position} onChange={handleChange} placeholder="Position" required style={{ padding: "8px", border: "1px solid #ccc", borderRadius: "4px" }} />
                <button type="submit" disabled={loading} style={{ padding: "10px", backgroundColor: "blue", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>
                    {loading ? "Adding..." : "Add Candidate"}
                </button>
            </form>
        </div>
    );
};

export default AddCandidate;
