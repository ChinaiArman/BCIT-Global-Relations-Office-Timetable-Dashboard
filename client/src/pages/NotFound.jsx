// pages/NotFound.jsx
import React from 'react';
import ErrorDisplay from '../components/ErrorDisplay';

const NotFound = () => {
    return (
        <main className="mx-auto flex min-h-screen w-full items-center justify-center bg-gray-900 text-white">
            <ErrorDisplay 
                errorCode="404"
                title="Page Not Found"
                description="Sorry, the page you're looking for isn't there."
                buttonText="BACK HOME"
                buttonLink="/"
                helpText="If you believe this is a mistake, please contact support or try again later."
            />
        </main>
    );
};

export default NotFound;