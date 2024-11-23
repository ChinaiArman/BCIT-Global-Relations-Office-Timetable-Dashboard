// components/LoginForm.jsx
import { useState } from 'react';
import axios from 'axios';
import { AlertCircle, X } from 'lucide-react';

const LoginForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const serverUrl = import.meta.env.VITE_SERVER_URL;
            const response = await axios.post(
                `${serverUrl}/api/authenticate/login/`,
                { email, password },
                { withCredentials: true }
            )
            if (response.status === 200) {
                console.log('Login successful:', response.data);
                window.location.href = '/';
            } else {
                setError('Incorrect username or password');
            }
        } catch (error) {
            setError('Incorrect username or password');
            console.error('Login failed:', error);
        }
    };

    return (
        <section className="flex w-[30rem] flex-col space-y-10">
            <div className="text-center text-4xl font-medium">Log In</div>
            
            {error && (
                <div className="flex items-center justify-between w-full p-4 mb-4 text-white bg-red-700 rounded-lg">
                    <div className="flex items-center">
                        <AlertCircle className="h-5 w-5 mr-2" />
                        <span>{error}</span>
                    </div>
                    <button 
                        onClick={() => setError('')} 
                        className="text-white focus:outline-none"
                    >
                        <X className="h-5 w-5" />
                    </button>
                </div>
            )}

            <form onSubmit={handleLogin} className="flex flex-col space-y-10">
                <div className="w-full transform border-b-2 bg-transparent text-lg duration-300 focus-within:border-indigo-500">
                    <input 
                        type="text" 
                        placeholder="Email or Username" 
                        className="w-full border-none bg-transparent outline-none placeholder:text-gray-500 focus:outline-none"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                
                <div className="w-full transform border-b-2 bg-transparent text-lg duration-300 focus-within:border-indigo-500">
                    <input 
                        type="password" 
                        placeholder="Password" 
                        className="w-full border-none bg-transparent outline-none placeholder:text-gray-500 focus:outline-none"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                
                <button 
                    type="submit"
                    className="transform rounded-sm bg-indigo-600 py-2 font-bold duration-300 hover:bg-indigo-400"
                >
                    LOG IN
                </button>
            </form>
            
            <a href="/verify" className="transform text-center font-semibold text-gray-500 duration-300 hover:text-gray-300">
                FIRST TIME LOGGING IN?
            </a>
            <a href="/forgot-password" className="transform text-center font-semibold text-gray-500 duration-300 hover:text-gray-300">
                FORGOT PASSWORD?
            </a>
        </section>
    );
};

export default LoginForm;

