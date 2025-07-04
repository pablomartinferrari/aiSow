// src/pages/AuthCallback.tsx
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthCallback: React.FC = () => {
    const navigate = useNavigate();

    useEffect(() => {
        // Get token from URL parameters
        const params = new URLSearchParams(window.location.search);
        const token = params.get('token');

        if (token) {
            localStorage.setItem('token', token);
            navigate('/', { replace: true });
        } else {
            navigate('/login', { replace: true });
        }
    }, [navigate]);

    return <div>Loading...</div>;
};

export default AuthCallback;
