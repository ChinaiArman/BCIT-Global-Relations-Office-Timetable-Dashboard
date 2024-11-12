import { useState } from 'react';
import axios from 'axios';

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleForgotPassword = async (e) => {
        e.preventDefault();
        try {
            const serverUrl = import.meta.env.VITE_SERVER_URL;
            const response = await axios.post(
                `${serverUrl}/api/authenticate/forgot-password/`,
                { email },
                { withCredentials: true }
            );
            
            if (response.status === 200) {
                setSuccess('Password reset instructions have been sent to your email');
                setError('');
            }
        } catch (error) {
            setError('Email not found. Please check and try again');
            setSuccess('');
            console.error('Forgot password request failed:', error);
        }
    };

    return (
        <main className="mx-auto flex min-h-screen w-full items-center justify-center bg-gray-900 text-white">
            <section className="flex w-[30rem] flex-col space-y-10">
                <div className="text-center text-4xl font-medium">Forgot Password</div>
                <p className="text-center text-gray-400">
                    Enter your email address and we'll send you instructions to reset your password.
                </p>

                {error && (
                    <div className="flex items-center justify-between w-full p-4 mb-4 text-white bg-red-700 rounded-lg">
                        <div className="flex items-center">
                            <svg 
                                xmlns="http://www.w3.org/2000/svg" 
                                className="h-5 w-5 mr-2 fill-current text-white"
                                viewBox="0 0 24 24"
                            >
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 15c-.83 0-1.5-.67-1.5-1.5S11.17 14 12 14s1.5.67 1.5 1.5S12.83 17 12 17zm1-4h-2V7h2v6z"/>
                            </svg>
                            <span>{error}</span>
                        </div>
                        <button 
                            onClick={() => setError('')} 
                            className="text-white focus:outline-none"
                        >
                            <svg 
                                xmlns="http://www.w3.org/2000/svg" 
                                className="h-5 w-5 fill-current text-white"
                                viewBox="0 0 24 24"
                            >
                                <path stroke="currentColor" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                )}

                {success && (
                    <div className="flex items-center justify-between w-full p-4 mb-4 text-white bg-green-600 rounded-lg">
                        <div className="flex items-center">
                            <svg 
                                xmlns="http://www.w3.org/2000/svg" 
                                className="h-5 w-5 mr-2 fill-current text-white"
                                viewBox="0 0 24 24"
                            >
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                            </svg>
                            <span>{success}</span>
                        </div>
                        <button 
                            onClick={() => setSuccess('')} 
                            className="text-white focus:outline-none"
                        >
                            <svg 
                                xmlns="http://www.w3.org/2000/svg" 
                                className="h-5 w-5 fill-current text-white"
                                viewBox="0 0 24 24"
                            >
                                <path stroke="currentColor" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
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
        </main>
    );
};

export default ForgotPassword;