import React, { useState, useEffect } from 'react';
import { PlusCircle, ChevronDown } from 'lucide-react';
import axios from 'axios';

const CourseColors = {
  'ACCG5150': { bg: 'bg-emerald-500/15', text: 'text-emerald-400', check: 'checked:bg-emerald-500', border: 'border-emerald-500/30' },
  'CHEM2214': { bg: 'bg-orange-500/15', text: 'text-orange-400', check: 'checked:bg-orange-500', border: 'border-orange-500/30' },
  'MATH1123': { bg: 'bg-sky-500/15', text: 'text-sky-400', check: 'checked:bg-sky-500', border: 'border-sky-500/30' },
  'PSYC2213': { bg: 'bg-violet-500/15', text: 'text-violet-400', check: 'checked:bg-violet-500', border: 'border-violet-500/30' },
  'MAN3145': { bg: 'bg-amber-500/15', text: 'text-amber-400', check: 'checked:bg-amber-500', border: 'border-amber-500/30' },
  'HIST1535': { bg: 'bg-rose-500/15', text: 'text-rose-400', check: 'checked:bg-rose-500', border: 'border-rose-500/30' },
  'BIO1345': { bg: 'bg-pink-500/15', text: 'text-pink-400', check: 'checked:bg-pink-500', border: 'border-pink-500/30' },
};

const TimeSlots = () => Array.from({ length: 22 }, (_, i) => i + 8);
const Days = () => ['MON', 'TUES', 'WED', 'THUR', 'FRI', 'SAT', 'SUN'];

const Schedule = () => [
  { course: 'ACCG5150', day: 'MON', startTime: 11.5, endTime: 13 },
  { course: 'MATH1123', day: 'TUES', startTime: 10, endTime: 11.5 },
  { course: 'PSYC2213', day: 'WED', startTime: 12, endTime: 13.5 },
  { course: 'PSYC2213', day: 'SAT', startTime: 12, endTime: 13.5 },
];

const CourseSelection = ({ course, isSelected, onToggle }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedGrouping, setSelectedGrouping] = useState('');
  const [groupings, setGroupings] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchCourseGroupings = async () => {
      if (isSelected && course.id) {
        setIsLoading(true);
        try {
          const serverUrl = import.meta.env.VITE_SERVER_URL;
          const response = await axios.get(
            `${serverUrl}/api/course/course_code/${course.id}/`,
            { withCredentials: true }
          );
          
          // Extract unique course groupings from the response
          const uniqueGroupings = [...new Set(response.data.map(course => course.course_grouping))];
          setGroupings(uniqueGroupings);
        } catch (error) {
          console.error('Error fetching course groupings:', error);
        } finally {
          setIsLoading(false);
        }
      }
    };

    fetchCourseGroupings();
  }, [isSelected, course.id]);

  return (
    <div className="flex items-center justify-between gap-2">
      <div className="flex items-center flex-1">
        <input
          type="checkbox"
          checked={isSelected}
          onChange={onToggle}
          className={`mr-3 h-4 w-4 rounded border-gray-700 ${CourseColors[course.id].check} focus:ring-offset-gray-900`}
        />
        <span className={`font-medium ${CourseColors[course.id].text}`}>{course.id}</span>
      </div>
      
      <div className="relative flex-1">
        <button
          onClick={() => isSelected && !isLoading && setIsOpen(!isOpen)}
          className={`w-full px-2 py-1 text-sm rounded flex items-center justify-between ${
            isSelected 
              ? `${CourseColors[course.id].bg} ${CourseColors[course.id].text} border ${CourseColors[course.id].border}`
              : 'bg-gray-800 text-gray-600 cursor-not-allowed'
          }`}
          disabled={!isSelected || isLoading}
        >
          <span>
            {isLoading ? 'Loading...' : selectedGrouping || 'Select Section'}
          </span>
          <ChevronDown className="w-4 h-4" />
        </button>
        
        {isOpen && isSelected && groupings.length > 0 && (
          <div className="absolute z-50 w-full mt-1 bg-gray-800 border border-gray-700 rounded-md shadow-lg">
            {groupings.map((grouping) => (
              <button
                key={grouping}
                className="w-full px-2 py-1 text-sm text-left text-gray-300 hover:bg-gray-700"
                onClick={() => {
                  setSelectedGrouping(grouping);
                  setIsOpen(false);
                }}
              >
                {grouping}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

const SchedulePage = () => {
  const [selectedCourses, setSelectedCourses] = useState([
    { id: 'ACCG5150', selected: true },
    { id: 'CHEM2214', selected: false },
    { id: 'MATH1123', selected: true },
    { id: 'PSYC2213', selected: true },
    { id: 'MAN3145', selected: false },
    { id: 'HIST1535', selected: false },
    { id: 'BIO1345', selected: false },
  ]);

  const [courseGroupings, setCourseGroupings] = useState({});

  const toggleCourse = (courseId) => {
    setSelectedCourses(selectedCourses.map(course => 
      course.id === courseId ? { ...course, selected: !course.selected } : course
    ));
  };

  useEffect(() => {
    const fetchCourseGroupings = async (courseId) => {
      try {
        const serverUrl = import.meta.env.VITE_SERVER_URL;
        const response = await axios.get(
          `${serverUrl}/api/course/course_id/${courseId}/`,
          { withCredentials: true }
        );
        
        // Assuming the response includes course_grouping data
        // Modify this according to your actual API response structure
        const uniqueGroupings = [...new Set(response.data.map(course => course.course_grouping))];
        setCourseGroupings(prev => ({
          ...prev,
          [courseId]: uniqueGroupings
        }));
      } catch (error) {
        console.error('Error fetching course groupings:', error);
      }
    };

    // Fetch groupings for selected courses
    selectedCourses.forEach(course => {
      if (course.selected && !courseGroupings[course.id]) {
        fetchCourseGroupings(course.id);
      }
    });
  }, [selectedCourses]);

  return (
    <div className='flex-1 overflow-auto relative z-10 bg-gray-900 text-white'>
      <div className="flex h-[calc(100vh-64px)]">
        {/* Left Sidebar */}
        <div className="w-64 bg-gray-900 border-r border-gray-800">
          <div className="p-6 h-full flex flex-col">
            <div className="mb-6">
              <h2 className="text-lg font-semibold mb-4 text-white">Student</h2>
              <div className="space-y-2">
                <p className="font-medium text-white">John Doe</p>
                <p className="text-sm text-gray-400">doe@my.bcit.ca</p>
                <p className="text-sm text-gray-400">University of Somewhere</p>
                <div className="flex items-center text-sm text-emerald-400 font-medium">
                  <span className="mr-1">●</span>
                  Schedule Finalized
                </div>
              </div>
            </div>

            <div className="flex-grow">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold text-white">Courses</h2>
                <button className="text-blue-400 hover:text-blue-300 transition-colors">
                  <PlusCircle className="w-5 h-5" />
                </button>
              </div>
              <div className="space-y-4">
                {selectedCourses.map((course) => (
                  <CourseSelection
                    key={course.id}
                    course={course}
                    isSelected={course.selected}
                    onToggle={() => toggleCourse(course.id)}
                    groupings={courseGroupings[course.id]}
                  />
                ))}
              </div>
            </div>

            <div className="mt-6">
              <h2 className="text-lg font-semibold mb-3 text-white">Conflicts</h2>
              <div className="text-sm text-red-400 font-medium">
                Thursday @11:30 - 12:30
              </div>
            </div>
          </div>
        </div>

        {/* Main Schedule Grid */}
        <div className="flex-1 p-6">
          <div className="bg-gray-900 border border-gray-800 rounded-lg h-full">
            <div className="grid grid-cols-8 h-full">
              {/* Time column */}
              <div className="col-span-1 border-r border-gray-800">
                <div className="h-12 sticky top-0 bg-gray-900 z-10"></div>
                {TimeSlots().map((time) => (
                  <div key={time} className="h-12 border-t border-gray-800 flex items-center justify-end pr-3 text-sm text-gray-400 font-medium">
                    {time}:30
                  </div>
                ))}
              </div>

              {/* Days columns */}
              {Days().map((day) => (
                <div key={day} className="col-span-1 border-r border-gray-800 last:border-r-0">
                  <div className="h-12 flex items-center justify-center font-medium sticky top-0 bg-gray-900 z-10 border-b border-gray-800 text-white">
                    {day}
                  </div>
                  <div className="relative">
                    {TimeSlots().map((time) => (
                      <div key={time} className="h-12 border-t border-gray-800"></div>
                    ))}
                    {Schedule()
                      .filter((event) => event.day === day)
                      .map((event, idx) => (
                        <div
                          key={idx}
                          className={`absolute w-11/12 left-1/2 -translate-x-1/2 ${CourseColors[event.course].bg} ${CourseColors[event.course].text} border ${CourseColors[event.course].border} rounded-lg p-2 text-sm font-medium flex items-center justify-center`}
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