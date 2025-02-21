// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App'; // Import the App component

const root = ReactDOM.createRoot(document.getElementById('root')); // Get the root element from the HTML
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
