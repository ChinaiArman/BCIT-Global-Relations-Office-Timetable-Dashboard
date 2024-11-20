import React, { useState } from "react";
import { AlertCircle, CheckCircle2 } from "lucide-react";
import UploadWindow from '../components/UploadWindow';
import DownloadWindow from '../components/DownloadWindow';  
import StatusMessage from '../components/StatusMessage';
import Header from "../components/Header";
import axios from 'axios';

const Database = () => {
  // Course states
  const [courseReplaceFile, setCourseReplaceFile] = useState(null);
  const [courseUpdateFile, setCourseUpdateFile] = useState(null);
  const [isCourseReplaceLoading, setIsCourseReplaceLoading] = useState(false);
  const [isCourseUpdateLoading, setIsCourseUpdateLoading] = useState(false);

  // Student states
  const [studentReplaceFile, setStudentReplaceFile] = useState(null);
  const [studentUpdateFile, setStudentUpdateFile] = useState(null);
  const [isStudentReplaceLoading, setIsStudentReplaceLoading] = useState(false);
  const [isStudentUpdateLoading, setIsStudentUpdateLoading] = useState(false);

  const [message, setMessage] = useState({ type: '', text: '' });

  const handleCourseReplace = async (e) => {
    e.preventDefault();
    if (!courseReplaceFile) {
      setMessage({ type: 'error', text: 'Please select an XLSX file to upload' });
      return;
    }
  
    const formData = new FormData();
    formData.append('file', courseReplaceFile);
    setIsCourseReplaceLoading(true);
  
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      const response = await axios.put(`${serverUrl}/api/course/import`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        withCredentials: true, // Include cookies with the request
      });
  
      const data = response.data;
  
      setMessage({
        type: 'success',
        text: data.message,
        details: data.invalid_rows?.length > 0
          ? `${data.invalid_rows.length} rows failed to upload.`
          : null,
      });
  
      setCourseReplaceFile(null);
      e.target.reset();
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.message || 'Error replacing course data',
      });
    } finally {
      setIsCourseReplaceLoading(false);
    }
  };

  const handleCourseUpdate = async (e) => {
    e.preventDefault();
    if (!courseUpdateFile) {
      setMessage({ type: 'error', text: 'Please select an XLSX file to upload' });
      return;
    }
  
    const formData = new FormData();
    formData.append('file', courseUpdateFile);
    setIsCourseUpdateLoading(true);
  
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      const response = await axios.patch(`${serverUrl}/api/course/import`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        withCredentials: true,
      });
  
      const data = response.data;
  
      setMessage({
        type: 'success',
        text: data.message,
        details: data.invalid_rows?.length > 0
          ? `${data.invalid_rows.length} rows failed to update.`
          : null,
      });
  
      setCourseUpdateFile(null);
      e.target.reset();
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.message || 'Error updating course data',
      });
    } finally {
      setIsCourseUpdateLoading(false);
    }
  };

  const handleTemplateDownload = async (apiURL, fileName) => { 
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      const response = await axios.get(`${serverUrl}${apiURL}`, {
        withCredentials: true, 
        responseType: 'blob'
      });
  
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement('a');
      a.href = url;
      a.download = fileName;
      document.body.appendChild(a); 
      a.click(); 
      a.remove(); 
  
      window.URL.revokeObjectURL(url);
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.message || 'Error downloading course template'
      });
    }
  };

  const handleStudentReplace = async (e) => {
    e.preventDefault();
    if (!studentReplaceFile) {
      setMessage({ type: 'error', text: 'Please select a CSV file to upload' });
      return;
    }
  
    const formData = new FormData();
    formData.append('file', studentReplaceFile);
    setIsStudentReplaceLoading(true);
  
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      const response = await axios.put(`${serverUrl}/api/student/import`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        withCredentials: true, // Include cookies with the request
      });
  
      const data = response.data;
  
      setMessage({
        type: 'success',
        text: data.message,
        details: data.invalid_rows?.length > 0
          ? `${data.invalid_rows.length} rows failed to upload.`
          : null,
      });
  
      setStudentReplaceFile(null);
      e.target.reset();
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.message || 'Error replacing student data',
      });
    } finally {
      setIsStudentReplaceLoading(false);
    }
  };

  const handleStudentUpdate = async (e) => {
    e.preventDefault();
    if (!studentUpdateFile) {
      setMessage({ type: 'error', text: 'Please select a CSV file to upload' });
      return;
    }
  
    const formData = new FormData();
    formData.append('file', studentUpdateFile);
    setIsStudentUpdateLoading(true);
  
    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      const response = await axios.patch(`${serverUrl}/api/student/import`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        withCredentials: true, // Include cookies with the request
      });
  
      const data = response.data;
  
      setMessage({
        type: 'success',
        text: data.message,
        details: data.invalid_rows?.length > 0
          ? `${data.invalid_rows.length} rows failed to update.`
          : null,
      });
  
      setStudentUpdateFile(null);
      e.target.reset();
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.message || 'Error updating student data',
      });
    } finally {
      setIsStudentUpdateLoading(false);
    }
  };

  return (
    <div className='flex-1 overflow-auto relative z-10 bg-gray-900 text-white'>
      <Header title='Database' />
      <main className='max-w-7xl mx-auto py-6 px-4 lg:px-8'>
        <div className="max-w-4xl mx-auto space-y-8">
          <h1 className="text-2xl font-bold mb-8">Courses</h1>
          <StatusMessage message={message} />
          
          <UploadWindow
            title="Replace Course Data"
            fileType="Course Data"
            fileExtension="XLSX"
            isLoading={isCourseReplaceLoading}
            selectedFile={courseReplaceFile}
            onFileChange={setCourseReplaceFile}
            onSubmit={handleCourseReplace}
          />
          
          <UploadWindow
            title="Update Course Data"
            fileType="Course Data"
            fileExtension="XLSX"
            isLoading={isCourseUpdateLoading}
            selectedFile={courseUpdateFile}
            onFileChange={setCourseUpdateFile}
            onSubmit={handleCourseUpdate}
          />
          
          <DownloadWindow
            title="Download Course Template"
            fileType="Course Template"
            fileExtension="XLSX"
            onClick={() => handleTemplateDownload("/api/course/download_template", "course_template.xlsx")}
          />

          <h1 className="text-2xl font-bold mb-8">Students</h1>
          
          <UploadWindow
            title="Replace Student Data"
            fileType="Student Data"
            fileExtension="CSV"
            isLoading={isStudentReplaceLoading}
            selectedFile={studentReplaceFile}
            onFileChange={setStudentReplaceFile}
            onSubmit={handleStudentReplace}
          />
          
          <UploadWindow
            title="Update Student Data"
            fileType="Student Data"
            fileExtension="CSV"
            isLoading={isStudentUpdateLoading}
            selectedFile={studentUpdateFile}
            onFileChange={setStudentUpdateFile}
            onSubmit={handleStudentUpdate}
          />

          <DownloadWindow
            title="Download Student Template"
            fileType="Student Template"
            fileExtension="CSV"
            onClick={() => handleTemplateDownload("/api/student/download_template", "student_template.csv")}
          />

          <h1 className="text-2xl font-bold mb-8">Schedules</h1>
          <DownloadWindow
            title="Download Schedule Data"
            fileType="Schedule Data"
            fileExtension="???"
            onClick={() => handleTemplateDownload("/api/student/download_template", "schedule_data.csv")}
          />
        </div>
      </main>
    </div>
  );
};

export default Database;