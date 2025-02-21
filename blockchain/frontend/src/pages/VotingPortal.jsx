import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function OnlinePreEnrollment() {
    const navigate = useNavigate();

    useEffect(() => {
        // Automatically navigate to login page as soon as this page is accessed
        navigate('/login');
    }, [navigate]);

    return null; // No content here, as we're redirecting to login
}

export default OnlinePreEnrollment;
