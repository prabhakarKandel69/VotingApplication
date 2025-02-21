// src/pages/Home.js
import React from "react";
import { Link } from "react-router-dom";
import "./Home.jsx"; // Optional: Add styling for the home page

function Home() {
  return (
    <div className="home">
      <h1>Welcome to the Election Commission</h1>
      <p>Explore the features and details here.</p>

      {/* Cards Section */}
      <div className="card-container">
        <Link to="/online-pre-enrollment">
          <div className="card">
            <h3>Online Pre-Enrollment</h3>
            <button>Get Started</button>
          </div>
        </Link>
        <Link to="/voter-roll">
          <div className="card">
            <h3>Check Voter Roll</h3>
            <button>View Details</button>
          </div>
        </Link>
        <Link to="/election-results">
          <div className="card">
            <h3>Election Results</h3>
            <button>View Results</button>
          </div>
        </Link>
        <Link to="/e-bulletin">
          <div className="card">
            <h3>E-Bulletin</h3>
            <button>Read Now</button>
          </div>
        </Link>
      </div>
    </div>
  );
}

export default Home;
