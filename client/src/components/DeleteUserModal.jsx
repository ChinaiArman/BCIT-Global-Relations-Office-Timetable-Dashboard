// components/DeleteUserModal.jsx
import React from 'react';
import { motion } from "framer-motion";
import { AlertCircle } from "lucide-react";

const DeleteUserModal = ({ isOpen, onClose, onConfirm, username }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50">
            <motion.div
                className="bg-gray-800 p-6 rounded-xl shadow-lg w-full max-w-md"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
            >
                <div className="flex flex-col items-center text-center">
                    <div className="flex items-center justify-center w-12 h-12 rounded-full bg-red-900/20 mb-4">
                        <AlertCircle className="w-6 h-6 text-red-500" />
                    </div>
                    
                    <h3 className="text-xl font-semibold text-gray-100 mb-2">
                        Confirm Delete
                    </h3>
                    
                    <p className="text-gray-400 mb-6">
                        Are you sure you want to delete the user <span className="font-semibold text-gray-300">{username}</span>? 
                        This action cannot be undone.
                    </p>

                    <div className="flex gap-3 w-full">
                        <button
                            onClick={onClose}
                            className="flex-1 px-4 py-2 rounded bg-gray-700 text-gray-300 hover:bg-gray-600 transition-colors"
                        >
                            Cancel
                        </button>
                        <button
                            onClick={onConfirm}
                            className="flex-1 px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700 transition-colors"
                        >
                            Delete
                        </button>
                    </div>
                </div>
            </motion.div>
        </div>
    );
};

export default DeleteUserModal;