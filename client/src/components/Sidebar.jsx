import { House, DatabaseZap, Menu, Settings, GraduationCap, ShieldCheck, CalendarCog } from "lucide-react";
import { useAdminAuth } from '../context/AdminContext.jsx';
import { useState, useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Link } from "react-router-dom";

const SIDEBAR_ITEMS = [
	{ name: "Home", icon: House, color: "#6366f1", href: "/" },
	{ name: "Students", icon: GraduationCap, color: "#8B5CF6", href: "/students" },
	{ name: "Scheduler", icon: CalendarCog, color: "#EC4899", href: "/scheduler" },
	{ name: "Database", icon: DatabaseZap, color: "#3B82F6", href: "/database" },
	{ name: "Settings", icon: Settings, color: "#6EE7B7", href: "/settings" },
];

const Sidebar = () => {
	const [isSidebarOpen, setIsSidebarOpen] = useState(true);
	const { isAdmin } = useAdminAuth();
	const [sidebarItems, setSidebarItems] = useState(SIDEBAR_ITEMS);

	useEffect(() => {
		// Add "Admin" item only once when `isAdmin` becomes true
		if (isAdmin) {
			setSidebarItems(prevItems => {
				// Check if "Admin" item already exists before adding
				if (!prevItems.some(item => item.name === "Admin")) {
					return [
						...prevItems.slice(0, 4),
						{ name: "Admin", icon: ShieldCheck, color: "#F59E0B", href: "/admin" },
						...prevItems.slice(4),
					];
				}
				return prevItems; // Return the unchanged array if "Admin" already exists
			});
		}
	}, [isAdmin]); // Only runs when `isAdmin` changes

	return (
		<motion.div
			className={`relative z-10 transition-all duration-300 ease-in-out flex-shrink-0 ${
				isSidebarOpen ? "w-64" : "w-20"
			}`}
			animate={{ width: isSidebarOpen ? 256 : 80 }}
		>
			<div className='h-full bg-gray-800 bg-opacity-50 backdrop-blur-md p-4 flex flex-col border-r border-gray-700'>
				<motion.button
					whileHover={{ scale: 1.1 }}
					whileTap={{ scale: 0.9 }}
					onClick={() => setIsSidebarOpen(!isSidebarOpen)}
					className='p-2 rounded-full hover:bg-gray-700 transition-colors max-w-fit'
				>
					<Menu size={24} />
				</motion.button>

				<nav className='mt-8 flex-grow'>
					{sidebarItems.map((item) => (
						<Link key={item.href} to={item.href}>
							<motion.div className='flex items-center p-4 text-sm font-medium rounded-lg hover:bg-gray-700 transition-colors mb-2'>
								<item.icon size={20} style={{ color: item.color, minWidth: "20px" }} />
								<AnimatePresence>
									{isSidebarOpen && (
										<motion.span
											className='ml-4 whitespace-nowrap'
											initial={{ opacity: 0, width: 0 }}
											animate={{ opacity: 1, width: "auto" }}
											exit={{ opacity: 0, width: 0 }}
											transition={{ duration: 0.2, delay: 0.3 }}
										>
											{item.name}
										</motion.span>
									)}
								</AnimatePresence>
							</motion.div>
						</Link>
					))}
				</nav>
			</div>
		</motion.div>
	);
};
export default Sidebar;
