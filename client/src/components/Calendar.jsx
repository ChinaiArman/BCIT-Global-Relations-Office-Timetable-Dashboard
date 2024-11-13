const TimeSlots =  Array.from({ length: 15 }, (_, i) => i + 8);
const Days =  ['MON', 'TUES', 'WED', 'THUR', 'FRI', 'SAT', 'SUN'];
const isTimeSlotInConflict = (day, startTime, endTime) => {
    return conflicts.some(conflict => 
        conflict.day === day && 
        startTime < conflict.endTime && 
        endTime > conflict.startTime
    );
};


const Calendar = ({ courseSchedules }) => {
    console.log(courseSchedules);
    return (
        <></>
    )

    // return (
    //         <div className="flex-1 p-6 overflow-x-auto">
    //             <div className="bg-gray-900 border border-gray-800 rounded-lg h-full min-w-[1200px]">
    //                 <div className="grid grid-cols-8 h-full">
    //                     {/* Time column */}
    //                     <div className="col-span-1 border-r border-gray-800 flex flex-col" style={{ height: '100%' }}>
    //                         <div className="h-12 sticky top-0 bg-gray-900 z-10"></div>
    //                         {TimeSlots.map((time) => (
    //                             <div
    //                                 key={time}
    //                                 className="border-t border-gray-800 flex items-center justify-end pr-3 text-sm text-gray-400 font-medium flex-grow"
    //                             >
    //                                 {time}:30
    //                             </div>
    //                         ))}
    //                     </div>
    //                     {/* Days columns */}
    //                     {Days.map((day) => (
    //                         <div key={day} className="col-span-1 border-r border-gray-800 last:border-r-0 flex flex-col" style={{ height: '100%' }}>
    //                             <div className="h-12 flex items-center justify-center font-medium sticky top-0 bg-gray-900 z-10 border-b border-gray-800 text-white">
    //                                 {day}
    //                             </div>
    //                             <div className="relative flex flex-col flex-grow">
    //                                 {TimeSlots.map((time) => (
    //                                     <div key={time} className="h-12 border-t border-gray-800 flex-grow"></div>
    //                                 ))}
    //                                 {courseSchedules.filter((event) => event.day === day).map((event, idx) => {
    //                                     const hasConflict = isTimeSlotInConflict(event.day, event.startTime, event.endTime);
    //                                     return (
    //                                         <div
    //                                             key={idx}
    //                                             className={`absolute w-11/12 left-1/2 -translate-x-1/2 ${hasConflict ? 'bg-red-500/20 border-red-500' : CourseColors[event.course].bg} ${CourseColors[event.course].text} border rounded-lg p-2 text-sm font-medium flex items-center justify-center transition-colors duration-200 ${hasConflict ? 'shadow-lg shadow-red-500/20' : ''}`}
    //                                             style={{
    //                                                 top: `${(event.startTime - 8) * 48}px`,
    //                                                 height: `${(event.endTime - event.startTime) * 48}px`,
    //                                             }}
    //                                         >
    //                                             <div className="text-center">
    //                                                 <div className="font-semibold">{event.course}</div>
    //                                                 <div className="text-xs opacity-75">{event.grouping}</div>
    //                                                 <div className="text-xs opacity-75">{event.room}</div>
    //                                             </div>
    //                                         </div>
    //                                     );
    //                                 })}
    //                             </div>
    //                         </div>
    //                     ))}
    //                 </div>
    //             </div>
    //         </div>
    // );
};

export default Calendar;