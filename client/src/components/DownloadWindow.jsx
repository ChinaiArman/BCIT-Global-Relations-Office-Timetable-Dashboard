import React from 'react';
import { Download } from 'lucide-react';
import { motion } from 'framer-motion';

const DownloadWindow = ({ 
  title, 
  fileType, 
  fileExtension, 
  onClick
}) => {
  return (
    <motion.div
      className="bg-gray-800 rounded-lg p-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
    >
      <h2 className="text-xl font-semibold mb-4">{title}</h2>
      <div className="space-y-4">
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300">
            {fileType} Template ({fileExtension})
          </label>
        </div>
        <button
          type="button"
          onClick={onClick}
          className={"flex items-center justify-center w-full px-4 py-2 rounded-md bg-indigo-600 hover:bg-indigo-500 text-white"}
        >
          <Download className="w-5 h-5 mr-2" />
          {`Download ${fileType}`}
        </button>
      </div>
    </motion.div>
  );
};

export default DownloadWindow;