import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
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
import ForgotPassword from './pages/ForgotPassword.jsx';
import Students from './pages/Students.jsx';

const App = () => {
    return (
        <UnverifiedAuthProvider>
            <VerifiedAuthProvider>
                <AdminAuthProvider>
                    <Router>
                        <Routes>
                            {/* Public Routes */}
                            <Route path="/login" element={<Login />} />
                            <Route path="/verify" element={<Verify />} />
                            <Route path="/forgot-password" element={<ForgotPassword />} />

                            {/* Protected Routes */}
                            <Route
                                path="/"
                                element={
                                    <PrivateRoute role="verified">
                                        <Dashboard />
                                    </PrivateRoute>
                                }
                            />
                            <Route
                                path="/scheduler"
                                element={
                                    <PrivateRoute role="verified">
                                        <Scheduler />
                                    </PrivateRoute>
                                }
                            />
                            <Route
                                path="/admin"
                                element={
                                    <PrivateRoute role="admin">
                                        <Admin />
                                    </PrivateRoute>
                                }
                            />
                            <Route
                                path="/settings"
                                element={
                                    <PrivateRoute role="verified">
                                        <Settings />
                                    </PrivateRoute>
                                }
                            />
                            <Route
                                path="/students"
                                element={
                                    <PrivateRoute role="admin">
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
    );
};

export default App;
