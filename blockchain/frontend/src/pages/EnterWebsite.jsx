import React from 'react';
import './EnterWebsite.css';

const EnterWebsite = () => {
    return (
        <div className="enter-website-container">
            <h1 className="enter-website-header">निर्वाचन आयोग, नेपाल</h1>
            <h2>Election Commission, Nepal</h2>

            <div className="enter-website-img-container">
                <img
                    src="https://via.placeholder.com/600x300" // Replace with your actual image source
                    alt="Election Commission Notification"
                    className="enter-website-img"
                />
                <p className="enter-website-description">
                    निर्वाचन स्मारिकाका लागि लेख रचना उपलब्ध गराउने सम्बन्धी सार्वजनिक सूचना
                </p>
            </div>

            <p className="enter-website-date">
                Date: २०८१/०९/१७ (2071-09-17)
            </p>
        </div>
    );
};

export default EnterWebsite;
