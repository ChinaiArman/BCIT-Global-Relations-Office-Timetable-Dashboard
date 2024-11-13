import React, { useState, useEffect } from 'react';
import { PlusCircle, ChevronDown } from 'lucide-react';
import axios from 'axios';

const CourseColors = {
  'ACCG5150': { bg: 'bg-emerald-500/15', text: 'text-emerald-400', check: 'checked:bg-emerald-500', border: 'border-emerald-500/30' },
  'MATH1310': { bg: 'bg-orange-500/15', text: 'text-orange-400', check: 'checked:bg-orange-500', border: 'border-orange-500/30' },
  'COMM1116': { bg: 'bg-sky-500/15', text: 'text-sky-400', check: 'checked:bg-sky-500', border: 'border-sky-500/30' },
  'ACIT3771': { bg: 'bg-violet-500/15', text: 'text-violet-400', check: 'checked:bg-violet-500', border: 'border-violet-500/30' },
  'ACIT3640': { bg: 'bg-amber-500/15', text: 'text-amber-400', check: 'checked:bg-amber-500', border: 'border-amber-500/30' },
  'HIST1535': { bg: 'bg-rose-500/15', text: 'text-rose-400', check: 'checked:bg-rose-500', border: 'border-rose-500/30' },
  'BIO1345': { bg: 'bg-pink-500/15', text: 'text-pink-400', check: 'checked:bg-pink-500', border: 'border-pink-500/30' },
};

const TimeSlots = () => Array.from({ length: 22 }, (_, i) => i + 8);
const Days = () => ['MON', 'TUES', 'WED', 'THUR', 'FRI', 'SAT', 'SUN'];

const dayMap = {
  'Mon': 'MON',
  'Tue': 'TUES',
  'Wed': 'WED',
  'Thu': 'THUR',
  'Fri': 'FRI',
  'Sat': 'SAT',
  'Sun': 'SUN'
};

const checkTimeOverlap = (event1, event2) => {
  const start1 = event1.startTime;
  const end1 = event1.endTime;
  const start2 = event2.startTime;
  const end2 = event2.endTime;
  
  return start1 < end2 && start2 < end1;
};

const formatTime = (time) => {
  const hours = Math.floor(time);
  const minutes = Math.round((time - hours) * 60);
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
};

const CourseSelection = ({ course, isSelected, onToggle, onGroupingSelect }) => {
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
            { 
              withCredentials: true,
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              }
            }
          );
          
          if (Array.isArray(response.data)) {
            const uniqueGroupings = [...new Set(response.data.map(course => course.course_grouping))];
            setGroupings(uniqueGroupings);
          }
        } catch (error) {
          console.error('Error fetching course groupings:', error);
        } finally {
          setIsLoading(false);
        }
      }
    };

    fetchCourseGroupings();
  }, [isSelected, course.id]);

  const handleGroupingSelect = async (grouping) => {
    setSelectedGrouping(grouping);
    setIsOpen(false);
    if (onGroupingSelect) {
      onGroupingSelect(course.id, grouping);
    }
  };

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
          <div className="absolute z-50 w-full mt-1 bg-gray-800 border border-gray-700 rounded-md shadow-lg max-h-48 overflow-y-auto">
            {groupings.map((grouping) => (
              <button
                key={grouping}
                className="w-full px-2 py-1 text-sm text-left text-gray-300 hover:bg-gray-700"
                onClick={() => handleGroupingSelect(grouping)}
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
    { id: 'MATH1310', selected: true },
    { id: 'COMM1116', selected: true },
    { id: 'ACIT3771', selected: true },
    { id: 'ACIT3640', selected: true },
    { id: 'HIST1535', selected: false },
    { id: 'BIO1345', selected: false },
  ]);

  const [courseSchedules, setCourseSchedules] = useState([]);
  const [conflicts, setConflicts] = useState([]);

  useEffect(() => {
    const newConflicts = [];
    
    for (let i = 0; i < courseSchedules.length; i++) {
      for (let j = i + 1; j < courseSchedules.length; j++) {
        const event1 = courseSchedules[i];
        const event2 = courseSchedules[j];
        
        if (event1.day === event2.day && checkTimeOverlap(event1, event2)) {
          newConflicts.push({
            day: event1.day,
            startTime: Math.min(event1.startTime, event2.startTime),
            endTime: Math.max(event1.endTime, event2.endTime),
            courses: [
              {
                id: event1.course,
                grouping: event1.grouping
              },
              {
                id: event2.course,
                grouping: event2.grouping
              }
            ]
          });
        }
      }
    }
    
    setConflicts(newConflicts);
  }, [courseSchedules]);

  const handleGroupingSelect = async (courseId, grouping) => {
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      const response = await axios.get(
        `${serverUrl}/api/course/course_grouping/${grouping}/`,
        { 
          withCredentials: true,
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }
      );

      if (Array.isArray(response.data)) {
        const newScheduleItems = response.data.map(course => {
          const [beginHour, beginMinute] = course.begin_time.split(':').map(Number);
          const [endHour, endMinute] = course.end_time.split(':').map(Number);
          
          const beginTime = beginHour + (beginMinute / 60);
          const endTime = endHour + (endMinute / 60);

          return {
            course: courseId,
            day: dayMap[course.day] || course.day.toUpperCase(),
            startTime: beginTime,
            endTime: endTime,
            grouping: course.course_grouping,
            room: course.building_room
          };
        });

        setCourseSchedules(prev => [
          ...prev.filter(schedule => schedule.course !== courseId),
          ...newScheduleItems
        ]);
      }
    } catch (error) {
      console.error('Error fetching course details:', error);
    }
  };

  const toggleCourse = (courseId) => {
    setSelectedCourses(selectedCourses.map(course => 
      course.id === courseId ? { ...course, selected: !course.selected } : course
    ));
    
    if (selectedCourses.find(c => c.id === courseId)?.selected) {
      setCourseSchedules(prev => prev.filter(schedule => schedule.course !== courseId));
    }
  };

  const isTimeSlotInConflict = (day, startTime, endTime) => {
    return conflicts.some(conflict => 
      conflict.day === day && 
      startTime < conflict.endTime && 
      endTime > conflict.startTime
    );
  };

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
                    onGroupingSelect={handleGroupingSelect}
                  />
                ))}
              </div>
            </div>

            <div className="mt-6">
              <h2 className="text-lg font-semibold mb-3 text-white">Conflicts</h2>
              <div className="space-y-2">
                {conflicts.length > 0 ? (
                  conflicts.map((conflict, index) => (
                    <div key={index} className="text-sm text-red-400 font-medium">
                      {conflict.day} @{formatTime(conflict.startTime)} - {formatTime(conflict.endTime)}
                      <div className="text-xs opacity-75 mt-1">
                        {conflict.courses.map(course => course.id).join(' & ')}
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-sm text-green-400 font-medium">
                    No conflicts detected
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

                {/* Main Schedule Grid */}
        <div className="flex-1 p-6 overflow-x-auto">
          <div className="bg-gray-900 border border-gray-800 rounded-lg h-full min-w-[1200px]">
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
                    {courseSchedules
                      .filter((event) => event.day === day)
                      .map((event, idx) => {
                        const hasConflict = isTimeSlotInConflict(event.day, event.startTime, event.endTime);
                        
                        return (
                          <div
                            key={idx}
                            className={`absolute w-11/12 left-1/2 -translate-x-1/2 
                              ${hasConflict ? 'bg-red-500/20 border-red-500' : CourseColors[event.course].bg} 
                              ${CourseColors[event.course].text} 
                              border 
                              rounded-lg p-2 text-sm font-medium flex items-center justify-center 
                              transition-colors duration-200
                              ${hasConflict ? 'shadow-lg shadow-red-500/20' : ''}`}
                            style={{
                              top: `${(event.startTime - 8) * 48}px`,
                              height: `${(event.endTime - event.startTime) * 48}px`,
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
      </div>
    </div>
  );
};

export default SchedulePage;



