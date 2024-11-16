import React, { useState } from "react";
import Header from "../components/Header";
import UserInfoCard from "../components/UserInfoCard";

const Settings = () => {
    return (
		<div className='flex-1 overflow-auto relative z-10 bg-gray-900'>
			<Header title='Settings' />
			<main className='max-w-4xl mx-auto py-6 px-4 lg:px-8'>
				<UserInfoCard />
			</main>
		</div>
	);
};

export default Settings;
