import React from 'react';

const NotFound = () => {
    return (
        <main className="mx-auto flex min-h-screen w-full items-center justify-center bg-gray-900 text-white">
            <section className="flex flex-col items-center space-y-8">
                {/* Large 404 Number */}
                <div className="text-9xl font-bold text-indigo-600">404</div>
                
                {/* SVG Icon */}
                <svg 
                    className="w-32 h-32 text-gray-600"
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24" 
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path 
                        strokeLinecap="round" 
                        strokeLinejoin="round" 
                        strokeWidth="2" 
                        d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                </svg>

                {/* Error Messages */}
                <div className="text-center space-y-4">
                    <h1 className="text-4xl font-bold text-white">Page Not Found</h1>
                    <p className="text-xl text-gray-400">Sorry, the page you're looking for isn't there.</p>
                </div>

                {/* Back to Login Button */}
                <a 
                    href="/login" 
                    className="transform rounded-sm bg-indigo-600 px-8 py-3 font-bold duration-300 hover:bg-indigo-400 text-center"
                >
                    BACK TO LOGIN
                </a>

                {/* Additional Help Text */}
                <p className="text-gray-500 text-sm text-center max-w-md">
                    If you believe this is a mistake, please contact support or try again later.
                </p>
            </section>
        </main>
    );
};

export default NotFound;