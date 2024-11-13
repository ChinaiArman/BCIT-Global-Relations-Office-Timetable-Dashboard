import Header from "../components/Header";
import UsersTable from "../components/UsersTable";

const Admin = () => {
    return (
		<div className='flex-1 overflow-auto relative z-10'>
			<Header title='Admin' />

			<main className='max-w-7xl mx-auto py-6 px-4 lg:px-8'>
				<UsersTable />
			</main>
		</div>
	);
};

export default Admin;
