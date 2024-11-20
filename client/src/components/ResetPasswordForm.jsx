import { useState } from 'react';
import axios from 'axios';

const ResetPasswordForm = ({ email }) => {
    const [code, setCode] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const passwordsMatch = newPassword && confirmPassword && newPassword === confirmPassword;

    const handleResetPassword = async (e) => {
        e.preventDefault();
        if (!passwordsMatch) {
            setError('Passwords do not match.');
            return;
        }

        try {
            const serverUrl = import.meta.env.VITE_SERVER_URL;
            const response = await axios.post(
                `${serverUrl}/api/authenticate/reset-password/`,
                { email, reset_code: code, password: newPassword },
                { withCredentials: true }
            );

            if (response.status === 200) {
                setSuccess('Password reset successful! You will automatically be redirected to the home page.');
                setError('');
            }
            setTimeout(() => {
                window.location.href = '/';
            }, 3000);
        } catch (error) {
            setError('Failed to reset password. Please try again.');
            setSuccess('');
            console.error('Password reset failed:', error);
        }
    };

    return (
        <section className="flex w-[30rem] flex-col space-y-10">
            <div className="text-center text-4xl font-medium">Reset Password</div>

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
                    type="text"
                    placeholder="Verification Code"
                    className="w-full border-none bg-transparent outline-none placeholder: focus:outline-none"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                />
            </div>

            <div className="w-full transform border-b-2 bg-transparent text-lg duration-300 focus-within:border-indigo-500">
                <input
                    type="password"
                    placeholder="New Password"
                    className="w-full border-none bg-transparent outline-none placeholder: focus:outline-none"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                />
            </div>

            <div className="w-full transform border-b-2 bg-transparent text-lg duration-300 focus-within:border-indigo-500">
                <input
                    type="password"
                    placeholder="Confirm New Password"
                    className="w-full border-none bg-transparent outline-none placeholder: focus:outline-none"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />
            </div>

            <button
                className={`transform rounded-sm py-2 font-bold duration-300 ${
                    passwordsMatch ? 'bg-indigo-600 hover:bg-indigo-400' : 'bg-gray-500 cursor-not-allowed'
                }`}
                onClick={handleResetPassword}
                disabled={!passwordsMatch}
            >
                RESET PASSWORD
            </button>
        </section>
    );
};

export default ResetPasswordForm;
