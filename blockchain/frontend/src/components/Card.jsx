import React from 'react';
import { Link } from 'react-router-dom';

const Card = ({ imageSrc, title, buttonText, navigateTo }) => {
    return (
        <div className="card">
            <img src={imageSrc} alt={title} />
            <h3>{title}</h3>
            {/* Wrap the button with Link to trigger page navigation */}
            <Link to={navigateTo}>
                <button>{buttonText}</button>
            </Link>
        </div>
    );
};

export default Card;
