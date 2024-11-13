import { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Search } from "lucide-react";
import { useNavigate } from "react-router-dom"; // Import useNavigate for routing

const UsersTable = () => {
	const [searchTerm, setSearchTerm] = useState("");
	const [userData, setUserData] = useState([]); // Store all fetched users
	const [filteredUsers, setFilteredUsers] = useState([]); // Store the filtered users for display
	const navigate = useNavigate(); // For navigating to the /students page

	useEffect(() => {
		// Fetch student data from the API
		const fetchStudentData = async () => {
			try {
				const serverUrl = import.meta.env.VITE_SERVER_URL;
				const response = await axios.get(`${serverUrl}/api/student/get-all`, {
					withCredentials: true,
				});
				const students = response.data.map((student) => ({
					id: student.id,
					name: `${student.first_name} ${student.last_name}`,
					email: student.email,
					// set status to Complete if student has courses, else set to Incomplete
					status: student.is_completed ? "Complete" : "Incomplete",
				}));
				console.log("Students:", students);
				setUserData(students);
				setFilteredUsers(students); // Initialize filtered users with all students
			} catch (error) {
				console.error("Error fetching student data:", error);
			}
		};
		fetchStudentData();
	}, []);

	const handleSearch = (e) => {
		const term = e.target.value.toLowerCase();
		setSearchTerm(term);
		const filtered = userData.filter(
			(user) => user.name.toLowerCase().includes(term) || user.email.toLowerCase().includes(term)
		);
		setFilteredUsers(filtered);
	};

	// Limit the displayed students to 5
	const studentsToDisplay = filteredUsers.slice(0, 5);

	// Handle redirect to /students
	const handleViewMore = () => {
		navigate("/students");
	};

	return (
		<motion.div
			className='bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700'
			initial={{ opacity: 0, y: 20 }}
			animate={{ opacity: 1, y: 0 }}
			transition={{ delay: 0.2 }}
		>
			<div className='flex justify-between items-center mb-6'>
				<h2 className='text-xl font-semibold text-gray-100'>Users</h2>
				<div className='relative'>
					<input
						type='text'
						placeholder='Search users...'
						className='bg-gray-700 text-white placeholder-gray-400 rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'
						value={searchTerm}
						onChange={handleSearch}
					/>
					<Search className='absolute left-3 top-2.5 text-gray-400' size={18} />
				</div>
			</div>

			<div className='overflow-x-auto'>
				<table className='min-w-full divide-y divide-gray-700'>
					<thead>
						<tr>
							<th className='px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider'>
								Name
							</th>
							<th className='px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider'>
								Student ID
							</th>
							<th className='px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider'>
								Email
							</th>
							<th className='px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider'>
								Schedule Status
							</th>
							<th className='px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider'>
								Actions
							</th>
						</tr>
					</thead>

					<tbody className='divide-y divide-gray-700'>
						{studentsToDisplay.map((user) => (
							<motion.tr
								key={user.id}
								initial={{ opacity: 0 }}
								animate={{ opacity: 1 }}
								transition={{ duration: 0.3 }}
							>
								<td className='px-6 py-4 whitespace-nowrap'>
									<div className='flex items-center'>
										<div className='flex-shrink-0 h-10 w-10'>
											<div className='h-10 w-10 rounded-full bg-gradient-to-r from-purple-400 to-blue-500 flex items-center justify-center text-white font-semibold'>
												{user.name.charAt(0)}
											</div>
										</div>
										<div className='ml-4'>
											<div className='text-sm font-medium text-gray-100'>{user.name}</div>
										</div>
									</div>
								</td>

								<td className='px-6 py-4 whitespace-nowrap'>
									<div className='text-sm text-gray-300'>{user.id}</div>
								</td>
								<td className='px-6 py-4 whitespace-nowrap'>
									<div className='text-sm text-gray-300'>{user.email}</div>
								</td>

								<td className='px-6 py-4 whitespace-nowrap'>
									<span
										className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
											user.status === "Complete"
												? "bg-green-800 text-green-100"
												: "bg-red-800 text-red-100"
										}`}
									>
										{user.status}
									</span>
								</td>

								<td className='px-6 py-4 whitespace-nowrap text-sm text-gray-300'>
									<button className='text-indigo-400 hover:text-indigo-300 mr-2'>Edit</button>
									<button className='text-red-400 hover:text-red-300'>Delete</button>
								</td>
							</motion.tr>
						))}
					</tbody>
				</table>
			</div>

			{/* View More Button */}
			{filteredUsers.length > 5 && (
				<div className='mt-4 text-center'>
					<button
						onClick={handleViewMore}
						className='bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700'
					>
						View More
					</button>
				</div>
			)}
		</motion.div>
	);
};
export default UsersTable;
