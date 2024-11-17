// pages/ForgotPassword.jsx
import React from 'react';
import ForgotPasswordForm from '../components/ForgotPasswordForm';

const ForgotPassword = () => {
    return (
        <main className="mx-auto flex min-h-screen w-full items-center justify-center bg-gray-900 text-white">
            <ForgotPasswordForm />
        </main>
    );
};

export default ForgotPassword;