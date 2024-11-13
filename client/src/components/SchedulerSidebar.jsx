import { useState, useEffect } from 'react';
import { ChevronDown, ChevronUp, PlusCircle, CalendarCheck, CalendarSearch } from 'lucide-react';
import axios from 'axios';

const CourseColors = [
    { bg: 'bg-emerald-500/15', text: 'text-emerald-400', check: 'checked:bg-emerald-500', border: 'border-emerald-500/30' },
    { bg: 'bg-orange-500/15', text: 'text-orange-400', check: 'checked:bg-orange-500', border: 'border-orange-500/30' },
    { bg: 'bg-sky-500/15', text: 'text-sky-400', check: 'checked:bg-sky-500', border: 'border-sky-500/30' },
    { bg: 'bg-violet-500/15', text: 'text-violet-400', check: 'checked:bg-violet-500', border: 'border-violet-500/30' },
    { bg: 'bg-amber-500/15', text: 'text-amber-400', check: 'checked:bg-amber-500', border: 'border-amber-500/30' },
    { bg: 'bg-rose-500/15', text: 'text-rose-400', check: 'checked:bg-rose-500', border: 'border-rose-500/30' },
    { bg: 'bg-pink-500/15', text: 'text-pink-400', check: 'checked:bg-pink-500', border: 'border-pink-500/30' },
    { bg: 'bg-lime-500/15', text: 'text-lime-400', check: 'checked:bg-lime-500', border: 'border-lime-500/30' },
    { bg: 'bg-indigo-500/15', text: 'text-indigo-400', check: 'checked:bg-indigo-500', border: 'border-indigo-500/30' }
];

const SchedulerSidebar = ({ studentInfo }) => (
    <div className="w-64 bg-gray-900 border-r border-gray-800 p-6 h-full flex flex-col">
        <StudentInfo studentInfo={studentInfo} />
        <CourseList studentInfo={studentInfo} />
        <ConflictList />
    </div>
);


const StudentInfo = ({ studentInfo }) => {
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isCompleted, setIsCompleted] = useState(studentInfo.is_completed); // Local state to track completion

    const markAsDone = async () => {
        setIsSubmitting(true);

        try {
            const response = await axios.post(
                `${import.meta.env.VITE_SERVER_URL}/api/student/flip-mark-done/${studentInfo.id}`,
                null,
                { withCredentials: true }
            );

            if (response.status === 200) {
                // Flip the completion status after successful API response
                setIsCompleted(prevState => !prevState);
                console.log('Student schedule status flipped');
            }
        } catch (error) {
            console.error('Error making POST request:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="mb-6 text-white">
            <div className="flex items-center space-x-4">
                {/* Profile picture */}
                <div className="flex-shrink-0 h-12 w-12 rounded-full bg-gradient-to-r from-purple-400 to-blue-500 flex items-center justify-center text-white font-semibold">
                    {studentInfo.first_name.charAt(0)}
                </div>

                {/* Student Info */}
                <div>
                    <p className="text-lg font-medium">{`${studentInfo.first_name} ${studentInfo.last_name}`}</p>
                    <p className="text-sm text-gray-400">{studentInfo.id}</p>
                    <p className="text-sm text-gray-400">{studentInfo.email}</p>
                </div>
            </div>

            {/* Status */}
            <div
                className={`text-sm font-medium flex items-center justify-center mt-3 ${
                    isCompleted ? 'text-emerald-400' : 'text-yellow-400'
                }`}
            >
                <span className="mr-1">
                    {isCompleted ? (
                        <CalendarCheck size={20} className="mr-2 text-emerald-400" />
                    ) : (
                        <CalendarSearch size={20} className="mr-2 text-yellow-400" />
                    )}
                </span>
                {isCompleted ? 'Schedule Finalized' : 'Schedule In Progress'}
            </div>

            {/* Mark Done Button */}
            <div className="mt-4 flex justify-center">
                <button
                    onClick={markAsDone}
                    className={`rounded-sm px-4 py-2 font-bold text-sm text-white duration-300 hover:bg-red-400 text-center ${
                        isCompleted ? 'bg-red-500' : 'bg-indigo-600'
                    }`}
                    disabled={isSubmitting}
                >
                    {isSubmitting ? 'Submitting...' : isCompleted ? 'MARK AS INCOMPLETE' : 'MARK AS DONE'}
                </button>
            </div>
        </div>
    );
};


const CourseList = ({ studentInfo }) => {
    const [groupings, setGroupings] = useState([]);
    const [isOpen, setIsOpen] = useState(false);
    const [selectedGrouping, setSelectedGrouping] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const fetchCourseGroupings = async (courseId) => {
        try {
            setIsLoading(true);
            const response = await axios.get(`${import.meta.env.VITE_SERVER_URL}/api/course/course_code/${courseId}`, { withCredentials: true });
            setGroupings([...new Set(response.data.map(course => course.course_grouping))]);
        } catch (error) {
            console.error('Error fetching course groupings:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleGroupingSelect = (grouping) => {
        setSelectedGrouping(grouping);
        setIsOpen(false);
    };

    return (
        <div className="flex-grow">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold text-white">Courses</h2>
                <button className="text-blue-400 hover:text-blue-300">
                    <PlusCircle className="w-5 h-5" />
                </button>
            </div>
            {studentInfo.preferences.map((courseId, index) => {
                // Get the color object from the CourseColors array based on the index
                const courseColor = CourseColors[index % CourseColors.length];
                return (
                    <CourseItem
                        key={courseId}
                        courseId={courseId}
                        courseColor={courseColor}
                    />
                );
            })}
        </div>
    );
};


const CourseItem = ({ courseId, courseColor }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [selectedGrouping, setSelectedGrouping] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [groupings, setGroupings] = useState({});

    // Fetch saved selection from localStorage on initial render
    useEffect(() => {
        const savedGrouping = localStorage.getItem(`selectedGrouping-${courseId}`);
        if (savedGrouping) {
            setSelectedGrouping(savedGrouping); // Restore selection if present
        }
    }, [courseId]);

    // Function to toggle the dropdown visibility
    const onOpen = async () => {
        setIsOpen(prev => !prev); // Toggle dropdown visibility
        if (!isOpen) {
            setIsLoading(true); // Show loading when opening dropdown
            try {
                // Fetch the groupings for the course from the API
                const response = await axios.get(
                    `${import.meta.env.VITE_SERVER_URL}/api/course/get-all-course-groupings-by-course-code/${courseId}`,
                    { withCredentials: true }
                );
                setGroupings(response.data); // Store groupings as an object
            } catch (error) {
                console.error("Error fetching groupings:", error);
            } finally {
                setIsLoading(false); // Hide loading after fetching
            }
        }
    };

    // Function to handle grouping selection
    const onGroupingSelect = (groupingId) => {
        setSelectedGrouping(groupingId); // Update the selected grouping
        localStorage.setItem(`selectedGrouping-${courseId}`, groupingId); // Save the selection to localStorage
        setIsOpen(false); // Close the dropdown after selection
    };

    return (
        <div>
            <div className="flex items-center justify-between gap-2 mt-4">
                <div className="flex items-center flex-1">
                    <input
                        type="checkbox"
                        className={`mr-3 h-4 w-4 rounded border-gray-700 ${courseColor.check} focus:ring-offset-gray-900`}
                    />
                    <span className={`font-medium ${courseColor.text}`}>{courseId}</span>
                </div>
                <div className="relative flex-1">
                    <button
                        onClick={onOpen} // Trigger onOpen to toggle the dropdown visibility
                        className={`w-full p-1 text-sm rounded flex items-center justify-center w-8 h-8 ${isOpen ? `${courseColor.bg} ${courseColor.text} border ${courseColor.border}` : 'bg-gray-800 text-gray-600 cursor-pointer'}`}
                    >
                        {isLoading ? (
                            <span className="text-sm text-gray-300">Loading...</span>
                        ) : isOpen ? (
                            <ChevronUp className="w-4 h-4 text-gray-300" />
                        ) : (
                            <ChevronDown className="w-4 h-4 text-gray-300" />
                        )}
                    </button>
                </div>
            </div>
            {isOpen && (
                <div className="mt-2 bg-gray-800 border border-gray-700 rounded-md shadow-lg max-h-48 overflow-y-auto">
                    <div className="p-2">
                        {Object.keys(groupings).map((groupingId) => (
                            <div key={groupingId} className="flex items-center">
                                <input
                                    type="radio"
                                    id={`grouping-${groupingId}`}
                                    name={`course-grouping-${courseId}`}
                                    value={groupingId}
                                    checked={selectedGrouping === groupingId}
                                    onChange={() => onGroupingSelect(groupingId)} // Handle selection
                                    className="mr-2 h-4 w-4 text-indigo-400"
                                />
                                <label
                                    htmlFor={`grouping-${groupingId}`}
                                    className="w-full px-2 py-1 text-sm text-left text-gray-300 hover:bg-gray-700"
                                >
                                    {groupingId} {/* Display the grouping ID (key) */}
                                </label>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

const ConflictList = () => {
    const [conflicts, setConflicts] = useState([]);

    useEffect(() => {
        // Fetch conflicts (placeholder)
        setConflicts([
            { day: 'Monday', startTime: '9:00', endTime: '10:00', courses: ['ACCT1515', 'MATH1310'] },
            { day: 'Wednesday', startTime: '11:00', endTime: '12:00', courses: ['COMM1116', 'ORGB1100'] },
        ]);
    }, []);

    return (
        <div className="mt-6">
            <h2 className="text-lg font-semibold mb-3 text-white">Conflicts</h2>
            <div className="space-y-2">
                {conflicts.length > 0 ? (
                    conflicts.map((conflict, index) => (
                        <div key={index} className="text-sm text-red-400 font-medium">
                            {conflict.day} @{conflict.startTime} - {conflict.endTime}
                            <div className="text-xs opacity-75 mt-1">
                                {conflict.courses.join(' & ')}
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="text-sm text-green-400 font-medium">No conflicts detected</div>
                )}
            </div>
        </div>
    );
};

export default SchedulerSidebar;
