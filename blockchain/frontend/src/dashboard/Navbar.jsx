// src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Add a CSS file for styling

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="navbar-left">
                <h1>Online Voting System</h1>
            </div>
            <div className="navbar-center">
                <ul>
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/search">Search</Link></li>
                    <li><Link to="/contact">Contact Us</Link></li>
                </ul>
            </div>
            <div className="navbar-right">
                <ul>
                    <li><Link to="/logout">Logout</Link></li>
                    <li><Link to="/admin-login">Admin Login</Link></li>
                </ul>
            </div>
        </nav>
    );
};

export default Navbar;
