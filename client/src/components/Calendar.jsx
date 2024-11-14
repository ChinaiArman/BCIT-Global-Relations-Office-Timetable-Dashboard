import React from 'react';

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

const Calendar = ({ courseSchedules }) => {
    const TimeSlots = Array.from({ length: 15 }, (_, i) => i + 8); // Time slots from 8:00 to 22:00
    const Days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'];

    // A function to check if two courses on the same day overlap (i.e., have a time conflict)
    const isTimeSlotInConflict = (day, startTime, endTime, conflicts, currentCourseCode) => {
        return conflicts.some(conflict =>
            conflict.day === day &&
            conflict.course !== currentCourseCode && // Exclude the current course from being compared with itself
            startTime < conflict.endTime &&
            endTime > conflict.startTime
        );
    };

    // This function will transform the course data into the structure needed for the calendar
    const parseCourseData = (courses) => {
        return courses.flatMap((course) => {
            return course.schedule.map((schedule) => {
                // Parse start and end times
                const startTime = parseTime(schedule.begin_time);
                const endTime = parseTime(schedule.end_time);

                // Get the color for this course directly from courseColor
                const courseColor = course.courseColor;

                // Return the event in a form that fits your calendar structure
                return {
                    course: course.courseCode,
                    grouping: course.groupingId,
                    room: schedule.building_room,
                    day: schedule.day.toUpperCase(), // Ensure it's uppercase for matching
                    startTime,
                    endTime,
                    color: courseColor // Attach the color
                };
            });
        });
    };

    // Helper function to parse the time (e.g., "09:30" -> 570 minutes)
    const parseTime = (time) => {
        const [hours, minutes] = time.split(":").map(Number);
        return hours * 60 + minutes; // Correctly returns minutes since midnight
    };

    // Parse the course data to make it ready for rendering
    const events = parseCourseData(courseSchedules);

    return (
        <div className="flex-1 p-6 overflow-x-auto">
            <div className="bg-gray-900 border border-gray-800 rounded-lg h-full min-w-[1200px]">
                <div className="grid grid-cols-8 h-full">
                    {/* Time column */}
                    <div className="col-span-1 border-r border-gray-800 flex flex-col" style={{ height: '100%' }}>
                        <div className="h-12 sticky top-0 bg-gray-900 z-10"></div>
                        {TimeSlots.map((time) => (
                            <div
                                key={time}
                                className="border-t border-gray-800 flex items-center justify-end pr-3 text-sm text-gray-400 font-medium flex-grow"
                            >
                                {time}:30
                            </div>
                        ))}
                    </div>

                    {/* Days columns */}
                    {Days.map((day) => (
                        <div key={day} className="col-span-1 border-r border-gray-800 last:border-r-0 flex flex-col" style={{ height: '100%' }}>
                            <div className="h-12 flex items-center justify-center font-medium sticky top-0 bg-gray-900 z-10 border-b border-gray-800 text-white">
                                {day}
                            </div>
                            <div className="relative flex flex-col flex-grow">
                                {TimeSlots.map((time) => (
                                    <div key={time} className="h-12 border-t border-gray-800 flex-grow"></div>
                                ))}
                                {events
                                    .filter((event) => event.day === day)
                                    .map((event, idx) => {
                                        const hasConflict = isTimeSlotInConflict(event.day, event.startTime, event.endTime, events, event.course);
                                        return (
                                            <div
                                                key={idx}
                                                className={`absolute w-11/12 left-1/2 -translate-x-1/2 ${hasConflict ? 'bg-red-500/20 border-red-500' : event.color.bg} ${hasConflict ? 'border-red-500' : event.color.border} text-white border rounded-lg p-2 text-sm font-medium flex items-center justify-center transition-colors duration-200 ${hasConflict ? 'shadow-lg shadow-red-500/20' : ''}`}
                                                style={{
                                                    top: `${(event.startTime - 8 * 60) * 48 / 60}px`, // Convert to pixels (48px per 30 minutes)
                                                    height: `${(event.endTime - event.startTime) * 48 / 60}px`, // Convert to pixels (48px per 30 minutes)
                                                }}
                                            >
                                                <div className="text-center">
                                                    <div className="font-semibold">{event.course}</div>
                                                    <div className="text-xs opacity-75">{event.grouping}</div>
                                                    <div className="text-xs opacity-75">{event.room}</div>
                                                </div>
                                            </div>
                                        );
                                    })}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Calendar;
