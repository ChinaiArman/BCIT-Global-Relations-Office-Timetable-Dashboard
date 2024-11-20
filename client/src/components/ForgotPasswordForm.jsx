import { useState } from 'react';
import axios from 'axios';
import ResetPasswordForm from './ResetPasswordForm';

const ForgotPasswordForm = () => {
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [showResetForm, setShowResetForm] = useState(false); // Toggle between forms

    const handleForgotPassword = async (e) => {
        e.preventDefault();
        try {
            const serverUrl = import.meta.env.VITE_SERVER_URL;
            const response = await axios.post(
                `${serverUrl}/api/authenticate/request-password-reset/`,
                { email },
                { withCredentials: true }
            );

            if (response.status === 200) {
                setSuccess('Password reset instructions have been sent to your email.');
                setError('');
                setShowResetForm(true); // Show reset password form
            }
        } catch (error) {
            setError('Email not found. Please check and try again.');
            setSuccess('');
            console.error('Forgot password request failed:', error);
        }
    };

    if (showResetForm) {
        return <ResetPasswordForm email={email} />;
    }

    return (
        <section className="flex w-[30rem] flex-col space-y-10">
            <div className="text-center text-4xl font-medium">Forgot Password</div>
            <p className="text-center text-gray-400">
                Enter your email address and we'll send you instructions to reset your password.
            </p>

            {error && (
                <div className="flex items-center justify-between w-full p-4 mb-4 text-white bg-red-700 rounded-lg">
                    <span>{error}</span>
                </div>
            )}

            {success && (
                <div className="flex items-center justify-between w-full p-4 mb-4 text-white bg-green-600 rounded-lg">
                    <span>{success}</span>
                </div>
            )}

            <div className="w-full transform border-b-2 bg-transparent text-lg duration-300 focus-within:border-indigo-500">
                <input
                    type="email"
                    placeholder="Email Address"
                    className="w-full border-none bg-transparent outline-none placeholder: focus:outline-none"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
            </div>

            <button
                className="transform rounded-sm bg-indigo-600 py-2 font-bold duration-300 hover:bg-indigo-400"
                onClick={handleForgotPassword}
            >
                SEND RESET INSTRUCTIONS
            </button>

            <a
                href="/login"
                className="transform text-center font-semibold text-gray-500 duration-300 hover:text-gray-300"
            >
                BACK TO LOGIN
            </a>
        </section>
    );
};

export default ForgotPasswordForm;
