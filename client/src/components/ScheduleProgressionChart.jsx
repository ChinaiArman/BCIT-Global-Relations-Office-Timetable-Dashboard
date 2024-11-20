import { useEffect, useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { motion } from "framer-motion";

const ScheduleProgressionChart = () => {
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`${import.meta.env.VITE_SERVER_URL}/api/database/schedule-progression`, {
					withCredentials: true,
				});
                const data = response.data;
                
                const totalStudents = data.total_students;
				const transformedData = data.schedule_progressions.map((item) => ({
					date: new Date(item.date.replace(" GMT", "")).toLocaleDateString("en-US", { month: "short", day: "numeric" }),
					approvalsPercentage: (item.num_approvals_from_program_heads / totalStudents) * 100,
					completionsPercentage: (item.num_schedules_completed / totalStudents) * 100,
				}));

                setChartData(transformedData);
            } catch (error) {
                console.error("Error fetching schedule progression data:", error);
            }
        };

        fetchData();
    }, []);

    return (
        <motion.div
            className="bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
        >
            <h2 className="text-xl font-semibold text-gray-100 mb-4">Schedule Progression</h2>
            <div className="h-[320px]">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                        <XAxis dataKey="date" stroke="#9CA3AF" />
                        <YAxis
                            stroke="#9CA3AF"
                            domain={[0, 100]}
                            tickFormatter={(value) => `${value}%`}
                        />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: "rgba(31, 41, 55, 0.8)",
                                borderColor: "#4B5563",
                            }}
                            itemStyle={{ color: "#E5E7EB" }}
                            formatter={(value) => `${value.toFixed(2)}%`}
                        />
                        <Line
                            type="monotone"
                            dataKey="approvalsPercentage"
                            name="Approvals"
                            stroke="#8B5CF6"
                            strokeWidth={2}
                            dot={{ fill: "#8B5CF6", strokeWidth: 2, r: 4 }}
                            activeDot={{ r: 8 }}
                        />
                        <Line
                            type="monotone"
                            dataKey="completionsPercentage"
                            name="Completions"
                            stroke="#22D3EE"
                            strokeWidth={2}
                            dot={{ fill: "#22D3EE", strokeWidth: 2, r: 4 }}
                            activeDot={{ r: 8 }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </motion.div>
    );
};

export default ScheduleProgressionChart;
