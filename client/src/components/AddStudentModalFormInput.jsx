import React from 'react';

export const AddStudentModalFormInput = ({ 
  label, 
  name, 
  error, 
  ...props 
}) => {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-300 mb-1">
        {label}
      </label>
      <input
        name={name}
        {...props}
        className={`w-full bg-gray-700 border rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
          error ? 'border-red-500' : 'border-gray-600'
        }`}
      />
      {error && <p className="mt-1 text-sm text-red-400">{error}</p>}
    </div>
  );
};

export const PreferenceInput = ({ 
  index, 
  value, 
  error, 
  onChange 
}) => {
  return (
    <div>
      <input
        type="text"
        name={`preference${index + 1}`}
        placeholder={`Preference ${index + 1}`}
        value={value}
        onChange={onChange}
        className={`w-full bg-gray-700 border rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
          error ? 'border-red-500' : 'border-gray-600'
        }`}
      />
      {error && <p className="mt-1 text-sm text-red-400">{error}</p>}
    </div>
  );
};

export default AddStudentModalFormInput;