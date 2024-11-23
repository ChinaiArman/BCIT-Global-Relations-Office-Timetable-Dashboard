// pages/Login.jsx
import React from 'react';
import LoginForm from '../components/LoginForm';

const Login = () => {
    return (
        <div className="mx-auto flex min-h-screen w-full items-center justify-center bg-gray-900 text-white">
            <LoginForm />
        </div>
    );
};

export default Login;