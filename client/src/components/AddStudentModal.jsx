import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { AlertCircle, X } from "lucide-react";

const AddStudentModal = ({ isOpen, onClose }) => {
  const [formData, setFormData] = useState({
    id: "",
    first_name: "",
    last_name: "",
    email: "",
    term_code: "",
    preferences: ["", "", "", "", "", "", "", ""] // 8 empty preferences
  });

  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      await axios.post(
        `${serverUrl}/api/student/`,
        {
          ...formData,
          preferences: formData.preferences.filter(pref => pref !== "") // Remove empty preferences
        },
        { withCredentials: true }
      );
      onClose(true); // true indicates successful submission
    } catch (error) {
      setError(error.response?.data?.message || "Error creating student");
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name.startsWith("preference")) {
      const index = parseInt(name.replace("preference", "")) - 1;
      const newPreferences = [...formData.preferences];
      newPreferences[index] = value;
      setFormData(prev => ({ ...prev, preferences: newPreferences }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  if (!isOpen) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm"
    >
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.95, opacity: 0 }}
        className="bg-gray-800 p-6 rounded-lg border border-gray-700 shadow-xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto"
      >
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-gray-100">Add New Student</h2>
          <button onClick={() => onClose(false)} className="text-gray-400 hover:text-gray-300">
            <X size={24} />
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded-lg text-red-100 flex items-center gap-2">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Student ID</label>
              <input
                type="text"
                name="id"
                required
                maxLength={9}
                value={formData.id}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Term Code</label>
              <input
                type="number"
                name="term_code"
                required
                value={formData.term_code}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">First Name</label>
              <input
                type="text"
                name="first_name"
                required
                maxLength={50}
                value={formData.first_name}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Last Name</label>
              <input
                type="text"
                name="last_name"
                required
                maxLength={50}
                value={formData.last_name}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-300 mb-1">Email</label>
              <input
                type="email"
                name="email"
                required
                maxLength={100}
                value={formData.email}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-300">Course Preferences</label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {formData.preferences.map((pref, index) => (
                <input
                  key={index}
                  type="text"
                  name={`preference${index + 1}`}
                  placeholder={`Preference ${index + 1}`}
                  value={pref}
                  onChange={handleChange}
                  maxLength={8}
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              ))}
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <button
              type="button"
              onClick={() => onClose(false)}
              className="px-4 py-2 rounded bg-gray-700 text-gray-300 hover:bg-gray-600 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 transition-colors"
            >
              Add Student
            </button>
          </div>
        </form>
      </motion.div>
    </motion.div>
  );
};

export default AddStudentModal;