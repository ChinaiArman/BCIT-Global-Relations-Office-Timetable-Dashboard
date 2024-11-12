import React, { useState } from 'react';

const SchedulePage = () => {
  const courseColors = {
    'COMM1113': { bg: 'bg-emerald-200', text: 'text-emerald-800', check: 'checked:bg-emerald-500' },
    'CHEM2214': { bg: 'bg-orange-200', text: 'text-orange-800', check: 'checked:bg-orange-500' },
    'MATH1123': { bg: 'bg-sky-200', text: 'text-sky-800', check: 'checked:bg-sky-500' },
    'PSYC2213': { bg: 'bg-violet-200', text: 'text-violet-800', check: 'checked:bg-violet-500' },
    'MAN3145': { bg: 'bg-amber-200', text: 'text-amber-800', check: 'checked:bg-amber-500' },
    'HIST1535': { bg: 'bg-rose-200', text: 'text-rose-800', check: 'checked:bg-rose-500' },
    'BIO1345': { bg: 'bg-pink-200', text: 'text-pink-800', check: 'checked:bg-pink-500' },
  };

  const [selectedCourses, setSelectedCourses] = useState([
    { id: 'COMM1113', selected: true },
    { id: 'CHEM2214', selected: false },
    { id: 'MATH1123', selected: true },
    { id: 'PSYC2213', selected: true },
    { id: 'MAN3145', selected: false },
    { id: 'HIST1535', selected: false },
    { id: 'BIO1345', selected: false },
  ]);

  const timeSlots = Array.from({ length: 19 }, (_, i) => i + 8); // 8:00 to 17:30
  const days = ['MON', 'TUES', 'WED', 'THUR', 'FRI', 'SAT', 'SUN'];

  const schedule = [
    { course: 'COMM1113', day: 'MON', startTime: 11.5, endTime: 13 },
    { course: 'MATH1123', day: 'TUES', startTime: 10, endTime: 11.5 },
    { course: 'PSYC2213', day: 'WED', startTime: 12, endTime: 13.5 },
    { course: 'PSYC2213', day: 'SAT', startTime: 12, endTime: 13.5 },
  ];

  const toggleCourse = (courseId) => {
    setSelectedCourses(selectedCourses.map(course => 
      course.id === courseId ? { ...course, selected: !course.selected } : course
    ));
  };

  return (
    <div className="flex flex-1 h-[calc(100vh-64px)] bg-gray-50">
      {/* Left Sidebar */}
      <div className="w-64 min-h-full bg-white border-r border-gray-200 flex-shrink-0">
        <div className="p-4 h-full flex flex-col">
          <div className="mb-6">
            <h2 className="text-lg font-semibold mb-2 text-gray-900">Student</h2>
            <div className="space-y-2">
              <p className="font-medium text-gray-900">John Doe</p>
              <p className="text-sm text-gray-700">doe@my.bcit.ca</p>
              <p className="text-sm text-gray-700">University of Somewhere</p>
              <div className="flex items-center text-sm text-emerald-600 font-medium">
                <span className="mr-1">●</span>
                Schedule Finalized
              </div>
            </div>
          </div>

          <div className="flex-grow">
            <div className="flex justify-between items-center mb-2">
              <h2 className="text-lg font-semibold text-gray-900">Courses</h2>
              <button className="text-blue-600 text-2xl hover:bg-blue-50 w-6 h-6 flex items-center justify-center rounded">+</button>
            </div>
            <div className="space-y-2">
              {selectedCourses.map((course) => (
                <div key={course.id} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={course.selected}
                    onChange={() => toggleCourse(course.id)}
                    className={`mr-2 h-4 w-4 rounded border-gray-300 ${courseColors[course.id].check} focus:ring-0`}
                  />
                  <span className={`font-medium ${courseColors[course.id].text}`}>{course.id}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="mb-4">
            <h2 className="text-lg font-semibold mb-2 text-gray-900">Conflicts</h2>
            <div className="text-sm text-red-600 font-medium">
              Thursday @11:30 - 12:30
            </div>
          </div>
        </div>
      </div>

      {/* Main Schedule Grid */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full p-6">
          <div className="bg-white rounded-lg shadow h-full">
            <div className="grid grid-cols-8 h-full">
              {/* Time column */}
              <div className="col-span-1 border-r">
                <div className="h-12 sticky top-0 bg-white z-10"></div>
                {timeSlots.map((time) => (
                  <div key={time} className="h-12 border-t flex items-center justify-end pr-2 text-sm text-gray-700 font-medium">
                    {time}:30
                  </div>
                ))}
              </div>

              {/* Days columns */}
              {days.map((day) => (
                <div key={day} className="col-span-1 border-r last:border-r-0">
                  <div className="h-12 flex items-center justify-center font-medium sticky top-0 bg-white z-10 border-b text-gray-900">
                    {day}
                  </div>
                  <div className="relative">
                    {timeSlots.map((time) => (
                      <div key={time} className="h-12 border-t"></div>
                    ))}
                    {schedule
                      .filter((event) => event.day === day)
                      .map((event, idx) => (
                        <div
                          key={idx}
                          className={`absolute w-11/12 left-1/2 -translate-x-1/2 ${courseColors[event.course].bg} ${courseColors[event.course].text} rounded-lg shadow-sm p-2 text-sm font-medium flex items-center justify-center`}
                          style={{
                            top: `${(event.startTime - 8) * 48}px`,
                            height: `${(event.endTime - event.startTime) * 48}px`,
                          }}
                        >
                          {event.course}
                        </div>
                      ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SchedulePage;