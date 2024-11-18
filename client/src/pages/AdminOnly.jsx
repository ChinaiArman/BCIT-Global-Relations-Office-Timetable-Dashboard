import React from 'react';
import { ShieldOff } from "lucide-react";

const Unauthorized = () => {
    return (
        <main className="mx-auto flex min-h-screen w-full items-center justify-center bg-gray-900 text-white">
            <section className="flex flex-col items-center space-y-8">
                {/* Large Number */}
                <div className="text-9xl font-bold text-indigo-600">403</div>
               
                {/* Icon */}
                <ShieldOff className="w-32 h-32 text-gray-600" />

                {/* Error Messages */}
                <div className="text-center space-y-4">
                    <h1 className="text-4xl font-bold text-white">Access Denied</h1>
                    <p className="text-xl text-gray-400">
                        Sorry, this page is restricted to administrators only.
                    </p>
                </div>

                {/* Back to Dashboard Button */}
                <a
                    href="/dashboard"
                    className="transform rounded-sm bg-indigo-600 px-8 py-3 font-bold duration-300 hover:bg-indigo-400 text-center"
                >
                    BACK TO DASHBOARD
                </a>

                {/* Additional Help Text */}
                <p className="text-gray-500 text-sm text-center max-w-md">
                    If you believe you should have access to this page, please contact your system administrator.
                </p>
            </section>
        </main>
    );
};

export default Unauthorized;