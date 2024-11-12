import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loginSuccess, setLoginSuccess] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const serverUrl = import.meta.env.VITE_SERVER_URL;

            // Send the login request
            const response = await axios.post(
                `${serverUrl}/api/authenticate/login/`,
                { email, password },
                { withCredentials: true }
            );

            if (response.status === 200) {
                console.log('Login successful:', response.data);
                setLoginSuccess(true); // Trigger redirect after successful login
            } else {
                console.error('Login failed:', response.data);
                setLoginSuccess(false);
            }
        } catch (error) {
            console.error('Login failed:', error);
            setLoginSuccess(false);
        }
    };

    // Redirect to home page when loginSuccess is true
    useEffect(() => {
        if (loginSuccess) {
            navigate('/', { replace: true });
        }
    }, [loginSuccess, navigate]);

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <input 
                    type="email" 
                    placeholder="Email" 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)} 
                    required
                />
                <input 
                    type="password" 
                    placeholder="Password" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)} 
                    required
                />
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;
