import React, { useState } from "react";
import UploadWindow from '../components/UploadWindow';
import MessageDisplay from '../components/MessageDisplay';
import DatabaseLayout from '../components/DatabaseLayout';

const Database = () => {
  const [courseFile, setCourseFile] = useState(null);
  const [studentFile, setStudentFile] = useState(null);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [isCourseLoading, setIsCourseLoading] = useState(false);
  const [isStudentLoading, setIsStudentLoading] = useState(false);

  const handleCourseUpload = async (e) => {
    e.preventDefault();
    if (!courseFile) {
      setMessage({ type: 'error', text: 'Please select an XLSX file to upload' });
      return;
    }

    const formData = new FormData();
    formData.append('file', courseFile);
    setIsCourseLoading(true);

    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      const response = await fetch(`${serverUrl}/api/course/import`, {
        method: 'PUT',
        body: formData,
        credentials: 'include'
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Error uploading course data');
      }

      setMessage({
        type: 'success',
        text: data.message,
        details: data.invalid_rows?.length > 0
          ? `${data.invalid_rows.length} rows failed to upload.`
          : null
      });
      setCourseFile(null);
      e.target.reset();
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.message || 'Error uploading course data'
      });
    } finally {
      setIsCourseLoading(false);
    }
  };

  const handleStudentUpload = async (e) => {
    e.preventDefault();
    if (!studentFile) {
      setMessage({ type: 'error', text: 'Please select a CSV file to upload' });
      return;
    }

    const formData = new FormData();
    formData.append('file', studentFile);
    setIsStudentLoading(true);

    try {
      const serverUrl = import.meta.env.VITE_SERVER_URL;
      const response = await fetch(`${serverUrl}/api/student/import`, {
        method: 'PUT',
        body: formData,
        credentials: 'include'
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Error uploading student data');
      }

      setMessage({
        type: 'success',
        text: data.message,
        details: data.invalid_rows?.length > 0
          ? `${data.invalid_rows.length} rows failed to upload.`
          : null
      });
      setStudentFile(null);
      e.target.reset();
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.message || 'Error uploading student data'
      });
    } finally {
      setIsStudentLoading(false);
    }
  };

  return (
    <DatabaseLayout>
      <MessageDisplay message={message} />
      <div className="space-y-6">
        <UploadWindow
          title="Upload Course Data"
          fileType="Course Data"
          fileExtension="XLSX"
          isLoading={isCourseLoading}
          selectedFile={courseFile}
          onFileChange={setCourseFile}
          onSubmit={handleCourseUpload}
        />
        <UploadWindow
          title="Upload Student Data"
          fileType="Student Data"
          fileExtension="CSV"
          isLoading={isStudentLoading}
          selectedFile={studentFile}
          onFileChange={setStudentFile}
          onSubmit={handleStudentUpload}
        />
      </div>
    </DatabaseLayout>
  );
};

export default Database;