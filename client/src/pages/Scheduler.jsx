import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Calendar from '../components/Calendar';
import SchedulerSidebar from '../components/SchedulerSidebar';

const SchedulePage = () => {
	const { studentId } = useParams();
	const [studentInfo, setStudentInfo] = useState({});
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const fetchData = async () => {
			try {
				const serverUrl = import.meta.env.VITE_SERVER_URL;
				const response = await axios.get(`${serverUrl}/api/student/${studentId}`, { withCredentials: true });
				setStudentInfo(response.data);
			} catch (error) {
				console.error('Error fetching data:', error);
			} finally {
				setLoading(false);
			}
		};

		fetchData();
	}, [studentId]);

	if (loading) {
		return <div>Loading...</div>;
	}

	return (
		<div className='flex-1 overflow-auto relative z-10 bg-gray-900 text-white'>
			<div className="flex h-[calc(100vh-64px)]">
				<SchedulerSidebar studentInfo={studentInfo} />
				<Calendar courseSchedules={studentInfo.courses} />
			</div>
		</div>
	);
};

export default SchedulePage;
