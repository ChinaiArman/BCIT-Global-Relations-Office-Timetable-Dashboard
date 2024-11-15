import { useState, useEffect } from "react";
import axios from "axios";
import { CalendarX, CalendarCheck, GraduationCap, CalendarSearch } from "lucide-react";
import { motion } from "framer-motion";

import Header from "../components/Header";
import StatCard from "../components/StatCard";
import StudentsTable from "../components/StudentsTable";
import UserGrowthChart from "../components/UserGrowthChart";
import UserActivityHeatmap from "../components/UserActivityHeatmap";
import UserDemographicsChart from "../components/UserDemographicsChart";

const Dashboard = () => {
	const [schedulingStats, setSchedulingStats] = useState({
		totalStudents: 0,
		totalSchedulesInProgress: 0,
		totalSchedulesFinalized: 0,
		totalStudentsWithoutCourses: 0,
	});
	const [loading, setLoading] = useState(true); 

	useEffect(() => {
		const fetchSchedulingStats = async () => {
			try {
				const serverUrl = import.meta.env.VITE_SERVER_URL;
				const response = await axios.get(`${serverUrl}/api/database/jumbotron`, {
					withCredentials: true,
				});

				if (response.status === 200) {
					const newData = {
						totalStudents: response.data.total_students,
						totalSchedulesInProgress: response.data.total_schedules_in_progress,
						totalSchedulesFinalized: response.data.total_schedules_finalized,
						totalStudentsWithoutCourses: response.data.total_students_without_course,
					}
					setSchedulingStats(newData);
				} else {
					console.error("Failed to fetch user stats:", response);
				}
			} catch (error) {
				console.error("Failed to fetch user stats:", error);
			} finally {
				setLoading(false);
			}
		};

		fetchSchedulingStats();
	}, []);

	return (
		<div className='flex-1 overflow-auto relative z-10 bg-gray-900 text-white'>
			<Header title='Dashboard' />

			<main className='max-w-7xl mx-auto py-6 px-4 lg:px-8'>
				{loading ? (
					<div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
						<p>Loading stats...</p>
					</div>
				) : (
					<motion.div
						className='grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8'
						initial={{ opacity: 0, y: 20 }}
						animate={{ opacity: 1, y: 0 }}
						transition={{ duration: 1 }}
					>
						{/* Stat Cards */}
						<StatCard
							name='Total Students'
							icon={GraduationCap}
							value={schedulingStats.totalStudents}
							color='#6366F1'
						/>
						<StatCard 
							name='Schedules Completed'
							icon={CalendarCheck}
							value={schedulingStats.totalSchedulesFinalized}
							color='#10B981' 
						/>
						<StatCard
							name='Schedules In Progress'
							icon={CalendarSearch}
							value={schedulingStats.totalSchedulesInProgress}
							color='#F59E0B'
						/>
						<StatCard
							name='Schedules Not Started'
							icon={CalendarX}
							value={schedulingStats.totalStudentsWithoutCourses}
							color='#EF4444'
						/>
					</motion.div>
				)}

				<StudentsTable isDashboard={true} />

				{/* USER CHARTS */}
				<div className='grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8'>
					<UserGrowthChart />
					<UserActivityHeatmap />
					<UserDemographicsChart />
				</div>
			</main>
		</div>
	);
};

export default Dashboard;
