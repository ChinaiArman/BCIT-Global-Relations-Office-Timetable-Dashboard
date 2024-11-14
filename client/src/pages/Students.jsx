import { motion } from "framer-motion";
import Header from "../components/Header";
import StudentsTable from "../components/StudentsTable";

const StudentsPage = () => {
  return (
    <div className="flex-1 overflow-auto relative z-10 bg-gray-900 text-white">
      <Header title="Students" />
      <main className="max-w-7xl mx-auto py-6 px-4 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <StudentsTable isDashboard={false} />
        </motion.div>
      </main>
    </div>
  );
};

export default StudentsPage;