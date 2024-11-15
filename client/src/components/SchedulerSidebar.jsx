import { useState, useEffect } from 'react';
import { PlusCircle, CalendarCheck, CalendarSearch } from 'lucide-react';
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

const SchedulerSidebar = ({ studentInfo, onSelectedCoursesChange }) => {
    const [selectedCourses, setSelectedCourses] = useState([]);

    const handleSelectedCoursesChange = (courses) => {
        setSelectedCourses(courses);
        onSelectedCoursesChange(courses); // Pass the selected courses to parent
    };

    return (
        <div className="w-64 bg-gray-900 border-r border-gray-800 p-6 min-h-screen flex flex-col">
            <StudentInfo studentInfo={studentInfo} selectedCourses={selectedCourses} />
            <CourseList
                studentInfo={studentInfo}
                onSelectedCoursesChange={handleSelectedCoursesChange} // Pass the handler to CourseList
            />
            <ConflictList selectedCourses={selectedCourses} />
        </div>
    );
};


const StudentInfo = ({ studentInfo, selectedCourses }) => {
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
            }
        } catch (error) {
            console.error('Error making POST request:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    const uploadCourseGroupings = async () => {
        const groupingIds = selectedCourses.map(course => course.groupingId);
        try {
            const response = await axios.put(`${import.meta.env.VITE_SERVER_URL}/api/student/replace-course-groupings/${studentInfo.id}`, { "course_groupings": groupingIds },{ withCredentials: true });
            if (response.status === 200) {
                console.log('Course groupings uploaded successfully');
            }
        } catch (error) {
            console.error('Error uploading course groupings:', error);
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
                    className={`rounded-sm px-4 py-2 font-bold text-sm text-white duration-300 text-center ${
                        isCompleted ? 'bg-red-500 hover:bg-red-400' : 'bg-indigo-600 hover:bg-indigo-500'
                    }`}
                    disabled={isSubmitting}
                >
                    {isSubmitting ? 'Submitting...' : isCompleted ? 'MARK AS INCOMPLETE' : 'MARK AS DONE'}
                </button>
            </div>

            {/* Save Button */}
            <div className="mt-4 flex justify-center">
                <button
                    onClick={uploadCourseGroupings}
                    className="rounded-sm px-4 py-2 font-bold text-sm text-white duration-300 hover:bg-green-400 text-center bg-green-600"
                >
                    Save
                </button>
            </div>
        </div>
    );
};


const CourseList = ({ studentInfo, onSelectedCoursesChange }) => {
    const [coursesState, setCoursesState] = useState(
        studentInfo.preferences.reduce((acc, courseCode) => {
            acc[courseCode] = {
                isOpen: false,
                selectedGrouping: '',
                isLoading: false,
                groupings: {},
            };
            return acc;
        }, {})
    );

    const allSelectedGroupingsHaveSchedules = () => {
        return Object.entries(coursesState).every(([courseCode, state]) => {
            const selectedGrouping = state.selectedGrouping;
            return selectedGrouping ? state.groupings[selectedGrouping] : true;
        });
    };

    useEffect(() => {
        if (allSelectedGroupingsHaveSchedules()) {
            const selectedCourses = Object.entries(coursesState)
                .filter(([, state]) => state.selectedGrouping)
                .map(([courseCode, state]) => ({
                    courseCode,
                    groupingId: state.selectedGrouping,
                    schedule: state.groupings[state.selectedGrouping],
                    courseColor: state.courseColor,
                }));

            onSelectedCoursesChange(selectedCourses);
        }
    }, [coursesState]); 

    const handleScheduleUpdate = (courseCode, groupingId, schedule) => {
        setCoursesState((prevState) => ({
            ...prevState,
            [courseCode]: {
                ...prevState[courseCode],
                groupings: {
                    ...prevState[courseCode].groupings,
                    [groupingId]: schedule,
                }
            }
        }));
    };

    const handleGroupingSelect = (courseCode, groupingId, courseColor) => {
        setCoursesState((prevState) => ({
            ...prevState,
            [courseCode]: {
                ...prevState[courseCode],
                selectedGrouping: groupingId,
                courseColor: courseColor,
            },
        }));
    };

    const toggleDropdown = async (courseCode, courseColor) => {
        setCoursesState((prevState) => ({
            ...prevState,
            [courseCode]: {
                ...prevState[courseCode],
                isOpen: !prevState[courseCode].isOpen,
                courseColor: courseColor,
            },
        }));

        if (!coursesState[courseCode].isOpen) {
            setCoursesState((prevState) => ({
                ...prevState,
                [courseCode]: { ...prevState[courseCode], isLoading: true },
            }));

            try {
                const response = await axios.get(
                    `${import.meta.env.VITE_SERVER_URL}/api/course/get-all-course-groupings-by-course-code/${courseCode}/${studentInfo.id}`,
                    { withCredentials: true }
                );
                const groupingsData = response.data;

                setCoursesState((prevState) => ({
                    ...prevState,
                    [courseCode]: {
                        ...prevState[courseCode],
                        groupings: groupingsData,
                        selectedGrouping: Object.keys(groupingsData)[0] || '',
                        isLoading: false,
                    },
                }));
            } catch (error) {
                console.error("Error fetching groupings:", error);
                setCoursesState((prevState) => ({
                    ...prevState,
                    [courseCode]: { ...prevState[courseCode], isLoading: false },
                }));
            }
        }
    };

    const removeCourse = (courseCode) => {
        setCoursesState((prevState) => ({
            ...prevState,
            [courseCode]: {
                ...prevState[courseCode],
                selectedGrouping: '', // Deselect the grouping
                isOpen: false, // Close the dropdown
            }
        }));
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold text-white">Courses</h2>
            </div>
            {studentInfo.preferences.map((courseCode, index) => {
                const courseColor = CourseColors[index % CourseColors.length];
                const courseState = coursesState[courseCode];

                return (
                    <CourseItem
                        key={courseCode}
                        courseCode={courseCode}
                        courseColor={courseColor}
                        isOpen={courseState.isOpen}
                        selectedGrouping={courseState.selectedGrouping}
                        isLoading={courseState.isLoading}
                        groupings={courseState.groupings}
                        onOpen={() => toggleDropdown(courseCode, courseColor)}
                        onGroupingSelect={(groupingId) => handleGroupingSelect(courseCode, groupingId, courseColor)}
                        onScheduleUpdate={(groupingId, schedule) => handleScheduleUpdate(courseCode, groupingId, schedule)}
                        onDeselectCourse={() => removeCourse(courseCode)}
                        isPreselected={studentInfo.course_codes.includes(courseCode)}
                        preselectedGrouping={studentInfo.course_codes.includes(courseCode) ? studentInfo.courses[courseCode] : ''}
                    />
                );
            })}
        </div>
    );
};


const CourseItem = ({
    courseCode,
    courseColor,
    isOpen,
    selectedGrouping,
    isLoading,
    groupings,
    onOpen,
    onGroupingSelect,
    onScheduleUpdate,
    onDeselectCourse,
    isPreselected,
    preselectedGrouping,
}) => {
    const [preselectionHandled, setPreselectionHandled] = useState(false);
    const [isChecked, setIsChecked] = useState(isPreselected);

    const handleCheckboxClick = (e) => {
        const isChecked = e.target.checked;
        setIsChecked(isChecked);

        if (isChecked) {
            // Open the dropdown and add the course to selectedCourses
            onOpen();
        } else {
            // Mark course as deselected
            onDeselectCourse();
        }
    };

    useEffect(() => {
        if (isPreselected && !preselectionHandled) {
            onOpen();
            onGroupingSelect(Object.keys(preselectedGrouping)[0]);

            if (!preselectedGrouping[Object.keys(preselectedGrouping)[0]]) {
                fetchSchedule(Object.keys(preselectedGrouping)[0]);
            }
            
            setPreselectionHandled(true);
            setIsChecked(true);
        }
    }, [isPreselected, preselectionHandled, onOpen, onGroupingSelect, preselectedGrouping]);

    return (
        <div>
            <div className="flex items-center justify-between gap-2 mt-4">
                <div className="flex items-center flex-1">
                    <input
                        type="checkbox"
                        className={`mr-3 h-4 w-4 rounded border-gray-700 ${courseColor.check} focus:ring-offset-gray-900`}
                        onChange={handleCheckboxClick}
                        checked={isChecked}
                    />
                    <span className={`font-medium ${courseColor.text}`}>{courseCode}</span>
                </div>
            </div>
            {isOpen && (
                <div className="mt-2 bg-gray-800 border border-gray-700 rounded-md shadow-lg max-h-48 overflow-y-auto">
                    {isLoading ? (
                        <div className="p-2 text-gray-300 text-center">Loading...</div>
                    ) : Object.keys(groupings).length === 0 ? (
                        <div className="p-2 text-gray-300 text-center">No groupings available</div>
                    ) : (
                        <div className="p-2">
                            {Object.keys(groupings).map((groupingId) => (
                                <div key={groupingId} className="flex items-center">
                                    <input
                                        type="radio"
                                        id={`grouping-${groupingId}`}
                                        name={`course-grouping-${courseCode}`}
                                        value={groupingId}
                                        checked={selectedGrouping === groupingId}
                                        onChange={() => onGroupingSelect(groupingId)}
                                        className="mr-2 h-4 w-4 text-indigo-400"
                                    />
                                    <label
                                        htmlFor={`grouping-${groupingId}`}
                                        className="w-full px-2 py-1 text-sm text-left text-gray-300 hover:bg-gray-700"
                                    >
                                        {groupingId}
                                    </label>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};


const ConflictList = ({ selectedCourses }) => {
    const [conflicts, setConflicts] = useState([]);

    useEffect(() => {
        const detectedConflicts = [];

        // Iterate over each course
        for (let i = 0; i < selectedCourses.length; i++) {
            for (let j = i + 1; j < selectedCourses.length; j++) {
                const courseA = selectedCourses[i];
                const courseB = selectedCourses[j];

                // Iterate over each schedule in course A and B
                for (let a = 0; a < courseA.schedule.length; a++) {
                    for (let b = 0; b < courseB.schedule.length; b++) {
                        const scheduleA = courseA.schedule[a];
                        const scheduleB = courseB.schedule[b];

                        // Check for day and time conflicts
                        if (scheduleA.day === scheduleB.day) {
                            const startA = parseTime(scheduleA.begin_time);
                            const endA = parseTime(scheduleA.end_time);
                            const startB = parseTime(scheduleB.begin_time);
                            const endB = parseTime(scheduleB.end_time);

                            if ((startA < endB) && (startB < endA)) {
                                detectedConflicts.push({
                                    day: scheduleA.day,
                                    startTime: scheduleA.begin_time,
                                    endTime: scheduleA.end_time,
                                    courses: [courseA.groupingId, courseB.groupingId], // Show grouping names
                                });
                            }
                        }
                    }
                }
            }
        }

        setConflicts(detectedConflicts);
    }, [selectedCourses]);

    return (
        <div className="mt-6 pb-5 flex-grow">
            <h2 className="text-lg font-semibold mb-3 text-white">Conflicts</h2>
            <div className="space-y-2">
                {conflicts.length > 0 ? (
                    conflicts.map((conflict, index) => (
                        <div key={index} className="text-sm text-red-400 font-medium">
                            {conflict.day} @{conflict.startTime} - {conflict.endTime}
                            <div className="text-xs opacity-75 mt-1">
                                {conflict.courses.join(' & ')}  {/* Displaying the grouping names */}
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

// Utility function to parse time in "HH:MM" format to a comparable number
function parseTime(timeString) {
    const [hours, minutes] = timeString.split(':').map(Number);
    return hours * 60 + minutes;
}

export default SchedulerSidebar;
