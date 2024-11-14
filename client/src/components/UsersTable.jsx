import { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Search, UserRoundPlus } from "lucide-react";

const UsersTable = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [userData, setUserData] = useState([]);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false); // State for controlling modal visibility
  const [newUser, setNewUser] = useState({
    username: "",
    email: "",
    password: "",
    verifyPassword: "",
  });

  const fetchUserData = async () => {
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      const response = await axios.get(`${serverUrl}/api/authenticate/get-users`, {
        withCredentials: true,
      });
      const users = response.data.map((user) => ({
        id: user.id,
        username: user.username,
        email: user.email,
        status: user.is_verified ? "Verified" : "Unverified",
        role: user.is_admin ? "Admin" : "User",
      }));
      setUserData(users);
      setFilteredUsers(users); // Initialize filtered users with all users
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  };

  useEffect(() => {
    fetchUserData();
  }, []);

  const handleSearch = (e) => {
    const term = e.target.value.toLowerCase();
    setSearchTerm(term);
    const filtered = userData.filter(
      (user) => user.username.toLowerCase().includes(term) || user.email.toLowerCase().includes(term)
    );
    setFilteredUsers(filtered);
  };


  // Handler for 'Change Role' button
  const handleRoleChange = async (user_id) => {
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      const response = await axios.patch(
        `${serverUrl}/api/authenticate/change-role/`,
        { user_id: user_id },
        { withCredentials: true }
      );
      console.log("Role Changed:", response.data);

      const updatedUsers = userData.map((user) => {
        if (user.id === user_id) {
          return {
            ...user,
            role: user.role === "Admin" ? "User" : "Admin",
          };
        }
        return user;
      });
      setUserData(updatedUsers);

      const updatedFilteredUsers = filteredUsers.map((user) => {
        if (user.id === user_id) {
          return {
            ...user,
            role: user.role === "Admin" ? "User" : "Admin",
          };
        }
        return user;
      });
      setFilteredUsers(updatedFilteredUsers);
    } catch (error) {
      console.error("Error changing role:", error);
    }
  };

  // Handler for 'Delete' button
  const handleDelete = async (userId) => {
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      const response = await axios.delete(`${serverUrl}/api/authenticate/delete-user/`, {
        withCredentials: true,
        data: { user_id: userId },
      });
      console.log("User deleted:", response.data);

      const updatedUsers = userData.filter((user) => user.id !== userId);
      const updatedFilteredUsers = filteredUsers.filter((user) => user.id !== userId);
      setUserData(updatedUsers);
      setFilteredUsers(updatedFilteredUsers);
    } catch (error) {
      console.error("Error deleting user:", error);
    }
  };

  // Handle modal close
  const closeModal = () => setIsModalOpen(false);

  // Handle modal form input
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewUser((prevUser) => ({
      ...prevUser,
      [name]: value,
    }));
  };

  // Handle adding a new user
  const handleAddUser = async () => {
    if (newUser.password !== newUser.verifyPassword) {
      alert("Passwords do not match!");
      return;
    }
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      const response = await axios.post(`${serverUrl}/api/authenticate/register/`, newUser, {
        withCredentials: true,
      });
      console.log("New user added:", response.data);

      closeModal();
      fetchUserData();
    } catch (error) {
      console.error("Error adding new user:", error);
    }
  };

  return (
    <motion.div
      className="bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
    >
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-gray-100">Users</h2>
        <div className="relative">
          <input
            type="text"
            placeholder="Search users..."
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
                Username
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                Email
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                Role
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>

          <tbody className="divide-y divide-gray-700">
            {filteredUsers.map((user) => (
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
                        {user.username.charAt(0)}
                      </div>
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-100">{user.username}</div>
                    </div>
                  </div>
                </td>

                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center text-sm text-gray-300">
                    <div className="mr-2">{user.email}</div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-800 text-blue-100">
                    {user.role}
                  </span>
                </td>

                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      user.status === "Verified"
                        ? "bg-green-800 text-green-100"
                        : "bg-red-800 text-red-100"
                    }`}
                  >
                    {user.status}
                  </span>
                </td>

                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                  <button
                    className="text-indigo-400 hover:text-indigo-300 mr-2"
                    onClick={() => handleRoleChange(user.id)}
                  >
                    Change Role
                  </button>
                  <button
                    className="text-red-400 hover:text-red-300"
                    onClick={() => handleDelete(user.id)}
                  >
                    Delete
                  </button>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-6 text-center">
        <button
          className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          onClick={() => setIsModalOpen(true)}
        >
          <UserRoundPlus className="mr-2" />
          Add New User
        </button>
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50">
          <motion.div
            className="bg-gray-800 p-6 rounded-xl shadow-lg w-full sm:w-1/3"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <h2 className="text-lg font-semibold text-gray-100 mb-4">Add New User</h2>

            <div className="mb-4">
              <label htmlFor="username" className="block text-sm font-medium text-gray-400">
                Username
              </label>
              <input
                type="text"
                id="username"
                name="username"
                className="mt-1 block w-full bg-gray-700 text-white rounded-lg p-2"
                value={newUser.username}
                onChange={handleInputChange}
              />
            </div>

            <div className="mb-4">
              <label htmlFor="email" className="block text-sm font-medium text-gray-400">
                Email
              </label>
              <input
                type="email"
                id="email"
                name="email"
                className="mt-1 block w-full bg-gray-700 text-white rounded-lg p-2"
                value={newUser.email}
                onChange={handleInputChange}
              />
            </div>

            <div className="mb-4">
              <label htmlFor="password" className="block text-sm font-medium text-gray-400">
                Password
              </label>
              <input
                type="password"
                id="password"
                name="password"
                className="mt-1 block w-full bg-gray-700 text-white rounded-lg p-2"
                value={newUser.password}
                onChange={handleInputChange}
              />
            </div>

            <div className="mb-4">
              <label htmlFor="verifyPassword" className="block text-sm font-medium text-gray-400">
                Verify Password
              </label>
              <input
                type="password"
                id="verifyPassword"
                name="verifyPassword"
                className="mt-1 block w-full bg-gray-700 text-white rounded-lg p-2"
                value={newUser.verifyPassword}
                onChange={handleInputChange}
              />
            </div>

            <div className="flex justify-between mt-6">
              <button
                onClick={closeModal}
                className="text-sm text-white bg-red-600 hover:bg-red-500 px-4 py-2 rounded-lg"
              >
              Cancel
              </button>
              <button
                onClick={handleAddUser}
                className="text-sm text-white bg-green-600 hover:bg-green-500 px-4 py-2 rounded-lg"
              >
                Add User
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </motion.div>
  );
};

export default UsersTable;
