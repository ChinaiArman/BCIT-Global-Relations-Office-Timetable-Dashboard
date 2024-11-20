import { useState, useEffect } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
import { Search, GraduationCap, AlertCircle } from "lucide-react";
import { Link } from "react-router-dom";
import AddStudentModal from "./AddStudentModal";

// Delete Modal Component
const DeleteModal = ({ isOpen, onClose, onConfirm, studentName }) => {
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
        className="bg-gray-800 p-6 rounded-lg border border-gray-700 shadow-xl w-full max-w-md mx-4"
      >
        <div className="flex items-center gap-3 mb-4">
          <AlertCircle className="text-red-400" size={24} />
          <h2 className="text-xl font-semibold text-gray-100">Confirm Deletion</h2>
        </div>
        
        <p className="text-gray-300 mb-6">
          Are you sure you want to delete {studentName}? This action cannot be undone.
        </p>
        
        <div className="flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded bg-gray-700 text-gray-300 hover:bg-gray-600 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className="px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700 transition-colors"
          >
            Delete
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
};

const StudentsTable = ({ isDashboard = false }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [userData, setUserData] = useState([]);
  const [filteredStudents, setFilteredStudents] = useState([]);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [studentToDelete, setStudentToDelete] = useState(null);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);

  const fetchStudents = async () => {
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      const response = await axios.get(`${serverUrl}/api/student/get-all`, {
        withCredentials: true,
      });
      const students = response.data.map((student) => ({
        id: student.id,
        name: `${student.first_name} ${student.last_name}`,
        email: student.email,
        schedule_status: student.is_completed 
          ? "Complete" 
          : student.course_codes.length === 0 
          ? "Incomplete" 
          : "In Progress",
        approval_status: student.is_approved_by_program_heads
          ? "Approved"
          : "Pending",
      }));
      setUserData(students);
      setFilteredStudents(students);
    } catch (error) {
      console.error("Error fetching student data:", error);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const handleSearch = (e) => {
    const term = e.target.value.toLowerCase();
    setSearchTerm(term);
    const filtered = userData.filter(
      (user) => user.name.toLowerCase().includes(term) || user.email.toLowerCase().includes(term)
    );
    setFilteredStudents(filtered);
  };

  const handleDeleteClick = (student) => {
    setStudentToDelete(student);
    setIsDeleteModalOpen(true);
  };

  const handleDeleteConfirm = async () => {
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      await axios.delete(`${serverUrl}/api/student/${studentToDelete.id}/`, {
        withCredentials: true,
      });
      await fetchStudents();
      setIsDeleteModalOpen(false);
      setStudentToDelete(null);
    } catch (error) {
      console.error("Error deleting student:", error);
      alert("Failed to delete student. Please try again.");
    }
  };

  const handleAddModalClose = (shouldRefetch = false) => {
    setIsAddModalOpen(false);
    if (shouldRefetch) {
      fetchStudents();
    }
  };

  const displayStudents = isDashboard 
    ? filteredStudents.slice(0, 5) 
    : filteredStudents;

  return (
    <>
      <motion.div
        className="bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-4">
            <h2 className="text-xl font-semibold text-gray-100">Students</h2>
              <div className=" flex justify-center">
                  <button
                      onClick={() => setIsAddModalOpen(true)}
                      className="rounded-sm w-42 px-4 py-2 font-bold text-sm text-white duration-300 text-center bg-indigo-600 hover:bg-indigo-500"
                  >
                    <div className="flex items-center justify-center gap-2">
                      <GraduationCap size={18} />
                      ADD STUDENT
                    </div>
                  </button>
              </div>
          </div>
          <div className="relative">
            <input
              type="text"
              placeholder="Search students..."
              className="bg-gray-700 text-white placeholder-gray-400 rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={searchTerm}
              onChange={handleSearch}
            />
            <Search className="absolute left-3 top-2.5 text-gray-400" size={18} />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-700">
            <thead>
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                  Student ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                  Email
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                  Schedule Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                  Approval Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>

            <tbody className="divide-y divide-gray-700">
              {displayStudents.map((user) => (
                <motion.tr
                  key={user.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.3 }}
                >
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10">
                        <div className="h-10 w-10 rounded-full bg-gradient-to-r from-purple-400 to-blue-500 flex items-center justify-center text-white font-semibold">
                          {user.name.charAt(0)}
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-100">{user.name}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-300">{user.id}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-300">{user.email}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        user.schedule_status === "Complete"
                          ? "bg-green-800 text-green-100"
                          : user.schedule_status === "Incomplete"
                          ? "bg-red-800 text-red-100"
                          : "bg-yellow-800 text-yellow-100"
                      }`}
                    >
                      {user.schedule_status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        user.approval_status === "Approved"
                          ? "bg-green-800 text-green-100"
                          : "bg-yellow-800 text-yellow-100"
                      }`}
                    >
                      {user.approval_status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    <a
                      href={`/scheduler/${user.id}`}
                      className="text-indigo-400 hover:text-indigo-300 mr-2"
                    >
                      Edit
                    </a>
                    <button 
                      className="text-red-400 hover:text-red-300"
                      onClick={() => handleDeleteClick(user)}
                    >
                      Delete
                    </button>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>

        {isDashboard && filteredStudents.length > 5 && (
          <div className="m-4 text-center">
            <Link 
              to="/students" 
              className="transform rounded-sm bg-indigo-600 px-8 py-3 font-bold duration-300 hover:bg-indigo-400 text-center"
            >
              VIEW MORE
            </Link>
          </div>
        )}
      </motion.div>

      <AnimatePresence>
        {isDeleteModalOpen && (
          <DeleteModal
            isOpen={isDeleteModalOpen}
            onClose={() => {
              setIsDeleteModalOpen(false);
              setStudentToDelete(null);
            }}
            onConfirm={handleDeleteConfirm}
            studentName={studentToDelete?.name}
          />
        )}
        {isAddModalOpen && (
          <AddStudentModal
            isOpen={isAddModalOpen}
            onClose={handleAddModalClose}
          />
        )}
      </AnimatePresence>
    </>
  );
};

export default StudentsTable;