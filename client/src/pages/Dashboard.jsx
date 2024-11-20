import { useState, useEffect } from "react";
import axios from "axios";
import { CalendarX, CalendarCheck, GraduationCap, CalendarSearch } from "lucide-react";
import { motion } from "framer-motion";

import Header from "../components/Header";
import StatCard from "../components/StatCard";
import StudentsTable from "../components/StudentsTable";
import ScheduleProgressionChart from "../components/ScheduleProgressionChart";
import CourseRankingTable from "../components/CourseRankingTable";

const Dashboard = () => {
	const [schedulingStats, setSchedulingStats] = useState({
		totalStudents: 0,
		totalSchedulesInProgress: 0,
		totalSchedulesFinalized: 0,
		totalStudentsWithoutCourses: 0,
	});
	const [popularPreferences, setPopularPreferences] = useState([]);
	const [popularCourses, setPopularCourses] = useState([]);

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
			}
		};
		const fetchPopularPreferences = async () => {
			try {
				const serverUrl = import.meta.env.VITE_SERVER_URL;
				const response = await axios.get(`${serverUrl}/api/database/most-popular-preferences`, {
					withCredentials: true,
				});

				if (response.status === 200) {
					setPopularPreferences(response.data);
				} else {
					console.error("Failed to fetch popular preferences:", response);
				}
			} catch (error) {
				console.error("Failed to fetch popular preferences:", error);
			}
		};
		const fetchPopularCourses = async () => {
			try {
				const serverUrl = import.meta.env.VITE_SERVER_URL;
				const response = await axios.get(`${serverUrl}/api/database/most-popular-course-registrations`, {
					withCredentials: true,
				});

				if (response.status === 200) {
					setPopularCourses(response.data);
				} else {
					console.error("Failed to fetch popular courses:", response);
				}
			} catch (error) {
				console.error("Failed to fetch popular courses:", error);
			}
		};

		fetchSchedulingStats();
		fetchPopularPreferences();
		fetchPopularCourses();
	}, []);

	return (
		<div className='flex-1 overflow-auto relative z-10 bg-gray-900 text-white'>
			<Header title='Dashboard' />

			<main className='max-w-7xl mx-auto py-6 px-4 lg:px-8'>
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

				<StudentsTable isDashboard={true} />

				{/* USER CHARTS */}
				<div className='mt-8'>
					<ScheduleProgressionChart />
				</div>
				<div className='grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8'>
					<CourseRankingTable tableTitle='Top 5 Courses' scoringColumnHeader='Total Students Enrolled' courseRankings={popularCourses} />
					<CourseRankingTable tableTitle='Top 5 Preferences' scoringColumnHeader='Average Preference Rank' courseRankings={popularPreferences}/>
				</div>
			</main>
		</div>
	);
};

export default Dashboard;
