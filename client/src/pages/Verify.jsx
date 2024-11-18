import React, { useState, useEffect } from 'react';
import { Shield, CheckCircle2, AlertCircle } from "lucide-react";
import { useParams } from 'react-router-dom';

const Verify = () => {
    const { code } = useParams();
    const [email, setEmail] = useState('');
    const [status, setStatus] = useState({ type: '', message: '' });
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        
        try {
            const serverUrl = import.meta.env.VITE_SERVER_URL;
            const response = await fetch(`${serverUrl}/api/authenticate/verify/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    verification_code: code,
                    email 
                }),
                credentials: 'include'
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Verification failed');
            }

            setStatus({
                type: 'success',
                message: 'Email verified successfully! You can now access your account.'
            });
        } catch (error) {
            setStatus({
                type: 'error',
                message: error.message || 'Failed to verify email'
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <main className="mx-auto flex min-h-screen w-full items-center justify-center bg-gray-900 text-white">
            <section className="flex flex-col items-center space-y-8 w-full max-w-md px-4">
                {/* Icon */}
                <Shield className="w-20 h-20 text-indigo-600" />

                {/* Title */}
                <div className="text-center space-y-2">
                    <h1 className="text-3xl font-bold text-white">Verify Your Email</h1>
                    <p className="text-gray-400">Please enter your email to complete verification</p>
                </div>

                {/* Status Message */}
                {status.message && (
                    <div className={`w-full p-4 rounded-md flex items-center space-x-2 ${
                        status.type === 'success' ? 'bg-green-900/50 text-green-400' : 'bg-red-900/50 text-red-400'
                    }`}>
                        {status.type === 'success' ? 
                            <CheckCircle2 className="shrink-0" size={20} /> : 
                            <AlertCircle className="shrink-0" size={20} />
                        }
                        <span>{status.message}</span>
                    </div>
                )}

                {/* Form */}
                <form onSubmit={handleSubmit} className="space-y-6 w-full">
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium text-gray-400 mb-1">
                            Email Address
                        </label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-600"
                            placeholder="Enter your email"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading}
                        className={`w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-700 rounded-md font-medium transition-colors
                            ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                    >
                        {isLoading ? 'Verifying...' : 'Verify Email'}
                    </button>
                </form>

                {/* Back Link */}
                <a
                    href="/login"
                    className="text-gray-400 hover:text-white text-sm transition-colors"
                >
                    Back to Login
                </a>
            </section>
        </main>
    );
};

export default Verify;