import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
    return (
        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
            <h1>Welcome to the Online Voting System</h1>
            <p>This is the home page. Navigate to the dashboard to explore more features.</p>
            <Link to="/dashboard">
                <button
                    style={{
                        padding: '0.5rem 1rem',
                        backgroundColor: 'blue',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer'
                    }}
                >
                    Go to Dashboard
                </button>
            </Link>
        </div>
    );
};

export default Home;
