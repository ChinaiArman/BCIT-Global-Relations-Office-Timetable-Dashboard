import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './components/Sidebar.jsx';
import { UnverifiedAuthProvider } from './context/UnverifiedAuthContext.jsx';
import { VerifiedAuthProvider } from './context/VerifiedAuthContext.jsx';
import { AdminAuthProvider } from './context/AdminContext.jsx';
import PrivateRoute from './components/PrivateRoute.jsx';
import Login from './pages/Login.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Scheduler from './pages/Scheduler.jsx';
import Admin from './pages/Admin.jsx';
import Settings from './pages/Settings.jsx';
import NotFound from './pages/NotFound.jsx';
import Verify from './pages/Verify.jsx';
import Database from './pages/Database.jsx';
import ForgotPassword from './pages/ForgotPassword.jsx';
import Students from './pages/Students.jsx';


const App = () => {
    return (
      <div className='flex h-screen bg-gray-900 text-gray-100 overflow-hidden'>
        <UnverifiedAuthProvider>
            <VerifiedAuthProvider>
                <AdminAuthProvider>
                    <Router>
                        <Routes>
                            {/* Public Routes */}
                            <Route path="/login" element={<Login />} />
                            <Route path="/forgot-password" element={<ForgotPassword />} />

                            {/* Protected Routes */}
                            <Route
                                path="/database"
                                element={
                                    <PrivateRoute role="verified">
                                        <Sidebar />
                                        <Database />
                                    </PrivateRoute>
                                }
                            />
                            <Route
                                path="/verify"
                                element={
                                    <PrivateRoute role="unverified">
                                        <Sidebar />
                                        <Verify />
                                    </PrivateRoute>
                                }
                            />
                            <Route
                                path="/"
                                element={
                                    <PrivateRoute role="verified">
                                        <Sidebar />
                                        <Dashboard />
                                    </PrivateRoute>
                                }
                            />
                            <Route
                                path="/scheduler/:studentId"
                                element={
                                    <PrivateRoute role="verified">
                                        <Sidebar />
                                        <Scheduler />
                                    </PrivateRoute>
                                }
                            />
                            <Route
                                path="/admin"
                                element={
                                    <PrivateRoute role="admin">
                                        <Sidebar />
                                        <Admin />
                                    </PrivateRoute>
                                }
                            />
                            <Route
                                path="/settings"
                                element={
                                    <PrivateRoute role="verified">
                                        <Sidebar />
                                        <Settings />
                                    </PrivateRoute>
                                }
                            />
                            <Route 
                                path="/authenticate/verify/:code?" 
                                element={
                                <Verify />
                                } />
                            <Route
                                path="/students"
                                element={
                                    <PrivateRoute role="verified">
                                        <Sidebar />
                                        <Students />
                                    </PrivateRoute>
                                }
                            />

                            {/* 404 Route */}
                            <Route path="*" element={<NotFound />} />
                        </Routes>
                    </Router>
                </AdminAuthProvider>
            </VerifiedAuthProvider>
        </UnverifiedAuthProvider>
      </div>
    );
};

export default App;
