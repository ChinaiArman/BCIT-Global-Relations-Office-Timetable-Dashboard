import { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Search } from "lucide-react";

const UsersTable = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [userData, setUserData] = useState([]);
  const [filteredUsers, setFilteredUsers] = useState([]);

  useEffect(() => {
    // Fetch user data from the API
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

  // Handler for 'Verify' button
  const handleVerify = async (email, username) => {
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL; 
      const response = await axios.post(
        `${serverUrl}/api/email/send-verification/`,
        { email: email, username: username }, 
        { withCredentials: true } 
      );
      console.log("Test email sent:", response.data);
    } catch (error) {
      console.error("Error sending test email:", error);
    }
  };

  // Handler for 'Test' button
  const handleTest = async (email) => {
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL; 
      const response = await axios.post(
        `${serverUrl}/api/email/test/`,
        { email: email }, 
        { withCredentials: true } 
      );
      console.log("Test email sent:", response.data);
    } catch (error) {
      console.error("Error sending test email:", error);
    }
  };

  // Handler for 'Delete' button
  const handleDelete = async (userId) => {
    try {
        const serverUrl = import.meta.env.VITE_SERVER_URL;
        const response = await axios.delete(`${serverUrl}/api/authenticate/delete-user/`, {
        withCredentials: true,
        data: {user_id: userId}
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
                    <button
                      className="text-indigo-400 hover:text-indigo-300 mr-2"
                      onClick={() => handleTest(user.email)}
                    >
                      Test
                    </button>
                    <button
                      className="text-green-400 hover:text-green-300"
                      onClick={() => handleVerify(user.email, user.username)}
                    >
                      Verify
                    </button>
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
                    onClick={() => handleTest(user.email)}
                  >
                    Edit
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
    </motion.div>
  );
};

export default UsersTable;
