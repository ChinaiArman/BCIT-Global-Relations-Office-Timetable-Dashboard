import { useState } from "react";
import { AlertCircle, X } from "lucide-react";
import { FormInput, PreferenceInput } from "./AddStudentModalFormInput";

const AddStudentModal = ({ isOpen, onClose }) => {
  const [formData, setFormData] = useState({
    id: "",
    first_name: "",
    last_name: "",
    email: "",
    term_code: "",
    preferences: ["", "", "", "", "", "", "", ""]
  });

  const [errors, setErrors] = useState({
    id: "",
    first_name: "",
    last_name: "",
    email: "",
    preferences: Array(8).fill("")
  });

  const [submitError, setSubmitError] = useState("");

  const validateField = (name, value) => {
    switch (name) {
      case 'id':
        return /^A\d{8}$/.test(value) 
          ? "" 
          : "ID must start with 'A' followed by exactly 8 numbers";
      
      case 'first_name':
      case 'last_name':
        return /^[A-Za-z]+$/.test(value) 
          ? "" 
          : "Only letters are allowed";
      
      case 'email':
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) 
          ? "" 
          : "Invalid email format";
      
      default:
        if (name.startsWith('preference')) {
          return value === "" || /^[A-Za-z]{4}\d{4}$/.test(value)
            ? ""
            : "Must be 4 letters followed by 4 numbers";
        }
        return "";
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const newErrors = {
      id: validateField('id', formData.id),
      first_name: validateField('first_name', formData.first_name),
      last_name: validateField('last_name', formData.last_name),
      email: validateField('email', formData.email),
      preferences: formData.preferences.map(pref => 
        pref ? validateField('preference', pref) : ""
      )
    };

    const hasErrors = Object.values(newErrors).some(error => 
      typeof error === 'string' ? error !== "" : error.some(e => e !== "")
    );

    if (hasErrors) {
      setErrors(newErrors);
      setSubmitError("Please fix the validation errors before submitting.");
      return;
    }

    try {
      const submissionData = {
        ...formData,
        preferences: formData.preferences.filter(pref => pref !== "")
      };
      
      onClose(true);
    } catch (error) {
      setSubmitError(error.response?.data?.message || "Error creating student");
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    if (name.startsWith("preference")) {
      const index = parseInt(name.replace("preference", "")) - 1;
      const newPreferences = [...formData.preferences];
      newPreferences[index] = value;
      
      const newPreferenceErrors = [...errors.preferences];
      newPreferenceErrors[index] = validateField('preference', value);
      
      setFormData(prev => ({ ...prev, preferences: newPreferences }));
      setErrors(prev => ({ ...prev, preferences: newPreferenceErrors }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
      setErrors(prev => ({ 
        ...prev, 
        [name]: validateField(name, value)
      }));
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm">
      <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 shadow-xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-gray-100">Add New Student</h2>
          <button onClick={() => onClose(false)} className="text-gray-400 hover:text-gray-300">
            <X size={24} />
          </button>
        </div>

        {submitError && (
          <div className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded-lg text-red-100 flex items-center gap-2">
            <AlertCircle size={20} />
            <span>{submitError}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormInput
              label="Student ID"
              name="id"
              required
              value={formData.id}
              onChange={handleChange}
              error={errors.id}
            />

            <FormInput
              label="Term Code"
              name="term_code"
              type="number"
              value={formData.term_code}
              onChange={handleChange}
            />

            <FormInput
              label="First Name"
              name="first_name"
              required
              value={formData.first_name}
              onChange={handleChange}
              error={errors.first_name}
            />

            <FormInput
              label="Last Name"
              name="last_name"
              required
              value={formData.last_name}
              onChange={handleChange}
              error={errors.last_name}
            />

            <div className="md:col-span-2">
              <FormInput
                label="Email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                error={errors.email}
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-300">Course Preferences</label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {formData.preferences.map((pref, index) => (
                <PreferenceInput
                  key={index}
                  index={index}
                  value={pref}
                  onChange={handleChange}
                  error={errors.preferences[index]}
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
      </div>
    </div>
  );
};

export default AddStudentModal;