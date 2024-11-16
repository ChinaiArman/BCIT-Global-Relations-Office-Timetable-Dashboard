import { useState, useEffect } from "react";
import { User, Lock } from "lucide-react";
import SettingSection from "./SettingSection";
import axios from "axios";

const initialProfileData = {
    username: "",
    email: "",
};

const UserInfoCard = () => {  
    const initialPasswordData = {
        oldPassword: "",
        password: "",
        confirmPassword: "",
    };

    const [profileData, setProfileData] = useState(initialProfileData);
    const [passwordData, setPasswordData] = useState(initialPasswordData);
    const [isEditingProfile, setIsEditingProfile] = useState(false);
    const [isEditingPassword, setIsEditingPassword] = useState(false);
    const [isProfileSaveEnabled, setIsProfileSaveEnabled] = useState(false);
    const [isPasswordSaveEnabled, setIsPasswordSaveEnabled] = useState(false);
    const [passwordsMatch, setPasswordsMatch] = useState(true);
    const [loading, setLoading] = useState(true); // To track loading state

    const getUserProfile = async () => {
        try {
            const serverUrl = import.meta.env.VITE_SERVER_URL;
            const response = await axios.get(`${serverUrl}/api/authenticate/get-user-info/`, {
                withCredentials: true,
            });

            console.log("User profile response:", response);

            if (response.status === 200) {
                const { name, email } = response.data.user;
                initialProfileData.username = name;
                initialProfileData.email = email;
                setProfileData({ username: name, email });
            }
        } catch (err) {
            console.error("Failed to get user profile:", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        getUserProfile();
    }, []);

    const handleProfileChange = (e) => {
        const { name, value } = e.target;
        setProfileData((prev) => ({
            ...prev,
            [name]: value,
        }));
        setIsProfileSaveEnabled(true);
    };

    const handlePasswordChange = (e) => {
        const { name, value } = e.target;
        setPasswordData((prev) => {
            const newData = { ...prev, [name]: value };

            if (name === "password") {
                setPasswordsMatch(value === newData.confirmPassword);
            } else if (name === "confirmPassword") {
                setPasswordsMatch(newData.password === value);
            }

            return newData;
        });
        if (passwordData.oldPassword && passwordData.password && passwordData.confirmPassword) {
            setIsPasswordSaveEnabled(true);
        }
    };

    const handleProfileSave = async (e) => {
        e.preventDefault();
        try {
            const serverUrl = import.meta.env.VITE_SERVER_URL;
            const response = await axios.put(`${serverUrl}/api/authenticate/update-user-info/`, profileData, {
                withCredentials: true,
            });

            if (response.status === 200) {
                initialProfileData.username = profileData.username;
                initialProfileData.email = profileData.email;
            }
        } catch (err) {
            console.error("Failed to update profile:", err);
        }

        setIsProfileSaveEnabled(false);
        setIsEditingProfile(false);
    };

    const handlePasswordSave = (e) => {
        e.preventDefault();
        console.log("Password data saved:", passwordData);

        try {
            const serverUrl = import.meta.env.VITE_SERVER_URL;
            axios.put(`${serverUrl}/api/authenticate/change-password/`, passwordData, {
                withCredentials: true,
            });
        } catch (err) { 
            console.error("Failed to update password:", err);
        }

        setIsPasswordSaveEnabled(false);
        setIsEditingPassword(false);
        setPasswordData(initialPasswordData);
    };

    const handleProfileCancel = () => {
        console.log("Profile data reset:", initialProfileData);
        setProfileData(initialProfileData);
        setIsEditingProfile(false);
        setIsProfileSaveEnabled(false);
    };

    const handlePasswordCancel = () => {
        setPasswordData(initialPasswordData);
        setIsEditingPassword(false);
        setIsPasswordSaveEnabled(false);
        setPasswordsMatch(true);
    };

    if (loading) {
        return <div>Loading...</div>; // Show loading text until profile is fetched
    }

    return (
        <div className="space-y-6">
            <SettingSection icon={User} title="Profile Information">
                <div className="flex flex-col sm:flex-row items-center mb-6">
                    <div>
                        <h3 className="text-lg font-semibold text-gray-100">{profileData.username}</h3>
                        <p className="text-gray-400">{profileData.email}</p>
                    </div>
                </div>

                {!isEditingProfile ? (
                    <button
                        onClick={() => setIsEditingProfile(true)}
                        className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition duration-200 w-full sm:w-auto"
                    >
                        Edit Profile
                    </button>
                ) : (
                    <form onSubmit={handleProfileSave} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-1">Username</label>
                            <input
                                type="text"
                                name="username"
                                value={profileData.username}
                                onChange={handleProfileChange}
                                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-1">Email</label>
                            <input
                                type="email"
                                name="email"
                                value={profileData.email}
                                onChange={handleProfileChange}
                                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>

                        <div className="flex justify-end gap-3 pt-4">
                            <button
                                type="button"
                                onClick={handleProfileCancel}
                                className="px-4 py-2 rounded bg-gray-600 text-gray-300 hover:bg-gray-500 transition-colors"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                disabled={!isProfileSaveEnabled}
                                className={`px-4 py-2 rounded ${isProfileSaveEnabled ? 'bg-blue-600 hover:bg-blue-700 text-white' : 'bg-gray-600 text-gray-300'} transition-colors`}
                            >
                                Save
                            </button>
                        </div>
                    </form>
                )}
            </SettingSection>

            <SettingSection icon={Lock} title="Change Password">
                {!isEditingPassword ? (
                    <button
                        onClick={() => setIsEditingPassword(true)}
                        className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition duration-200 w-full sm:w-auto"
                    >
                        Change Password
                    </button>
                ) : (
                    <form onSubmit={handlePasswordSave} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-1">Old Password</label>
                            <input
                                type="password"
                                name="oldPassword"
                                value={passwordData.oldPassword}
                                onChange={handlePasswordChange}
                                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-1">New Password</label>
                            <input
                                type="password"
                                name="password"
                                value={passwordData.password}
                                onChange={handlePasswordChange}
                                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-1">Confirm Password</label>
                            <input
                                type="password"
                                name="confirmPassword"
                                value={passwordData.confirmPassword}
                                onChange={handlePasswordChange}
                                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                            {!passwordsMatch && (
                                <p className="text-sm text-red-500 mt-1">Passwords do not match.</p>
                            )}
                        </div>

                        <div className="flex justify-end gap-3 pt-4">
                            <button
                                type="button"
                                onClick={handlePasswordCancel}
                                className="px-4 py-2 rounded bg-gray-600 text-gray-300 hover:bg-gray-500 transition-colors"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                disabled={!isPasswordSaveEnabled || !passwordsMatch}
                                className={`px-4 py-2 rounded ${isPasswordSaveEnabled && passwordsMatch ? 'bg-blue-600 hover:bg-blue-700 text-white' : 'bg-gray-600 text-gray-300'} transition-colors`}
                            >
                                Save
                            </button>
                        </div>
                    </form>
                )}
            </SettingSection>
        </div>
    );
};

export default UserInfoCard;
