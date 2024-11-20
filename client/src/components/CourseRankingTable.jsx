import { motion } from "framer-motion";

const CourseRankingTable = ({ tableTitle, scoringColumnHeader, courseRankings }) => {
  return (
    <motion.div
      className="bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
    >
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-gray-100 text-center w-full">
          {tableTitle}
        </h2>
      </div>

      <div className="overflow-x-auto">
        {courseRankings.length === 0 ? (
          <div className="text-center text-gray-400 py-6">
            No Data Available
          </div>
        ) : (
          <table className="min-w-full divide-y divide-gray-700 text-center">
            <thead>
              <tr>
                <th className="px-6 py-3 text-xs font-medium text-gray-400 uppercase tracking-wider">
                  Course Code
                </th>
                <th className="px-6 py-3 text-xs font-medium text-gray-400 uppercase tracking-wider">
                  {scoringColumnHeader}
                </th>
              </tr>
            </thead>

            <tbody className="divide-y divide-gray-700">
              {courseRankings.map((course, index) => {
                const courseCode = Object.keys(course)[0];
                const ranking = course[courseCode];

                return (
                  <motion.tr
                    key={index}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.3 }}
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-100">
                      {courseCode}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                      {ranking}
                    </td>
                  </motion.tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </motion.div>
  );
};

export default CourseRankingTable;
