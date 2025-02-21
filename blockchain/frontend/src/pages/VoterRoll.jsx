import { useEffect, useState } from "react";
import axios from "axios";

const VoterRoll = () => {
  const [voters, setVoters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedVoter, setSelectedVoter] = useState(null);
  const token = localStorage.getItem("accessToken"); // Authentication token

  useEffect(() => {
    // Fetch the list of voters from the backend using Axios
    axios
      .get("http://127.0.0.1:8000/voters/voters/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => {
        setVoters(response.data);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  const handleSelectVoter = (voter) => {
    setSelectedVoter(voter);
  };

  if (loading) {
    return <div>Loading voters...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h2>Voter Roll</h2>
      <table>
        <thead>
          <tr>
            <th>Voter ID</th>
            <th>Full Name</th>
            <th>Age</th>
            <th>Date of Birth</th>
            <th>Permanent Address</th>
            <th>Blood Group</th>
            <th>Voter Image</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {voters.map((voter) => (
            <tr key={voter.voter_id}>
              <td>{voter.voter_id}</td>
              <td>{voter.full_name}</td>
              <td>{voter.age}</td>
              <td>{voter.dob}</td>
              <td>{voter.permanent_address}</td>
              <td>{voter.blood_group}</td>
              <td>
                {voter.voter_image ? (
                  <img src={voter.voter_image} alt="Voter" width="50" />
                ) : (
                  "No image"
                )}
              </td>
              <td>
                <button onClick={() => handleSelectVoter(voter)}>Select</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selectedVoter && (
        <div>
          <h3>Selected Voter</h3>
          <p>
            Voter ID: {selectedVoter.voter_id}
            <br />
            Full Name: {selectedVoter.full_name}
            <br />
            Age: {selectedVoter.age}
            <br />
            Date of Birth: {selectedVoter.dob}
            <br />
            Permanent Address: {selectedVoter.permanent_address}
            <br />
            Blood Group: {selectedVoter.blood_group}
          </p>
        </div>
      )}
    </div>
  );
};

export default VoterRoll;
