import React from 'react';
import { Upload } from 'lucide-react';

const UploadWindow = ({ 
  title, 
  fileType, 
  fileExtension, 
  isLoading, 
  selectedFile, 
  onFileChange, 
  onSubmit 
}) => {
  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">{title}</h2>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300">
            {fileType} File ({fileExtension})
          </label>
          <input
            type="file"
            accept={`.${fileExtension.toLowerCase()}`}
            onChange={(e) => onFileChange(e.target.files[0])}
            className="block w-full text-sm text-gray-400
              file:mr-4 file:py-2 file:px-4
              file:rounded-md file:border-0
              file:text-sm file:font-medium
              file:bg-gray-700 file:text-gray-300
              hover:file:bg-gray-600
              cursor-pointer"
          />
        </div>
        <button
          type="submit"
          disabled={isLoading || !selectedFile}
          className={`flex items-center justify-center w-full px-4 py-2 rounded-md 
            ${isLoading || !selectedFile 
              ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-500 text-white'
            }`}
        >
          <Upload className="w-5 h-5 mr-2" />
          {isLoading ? 'Uploading...' : `Upload ${fileType}`}
        </button>
      </form>
    </div>
  );
};

export default UploadWindow;