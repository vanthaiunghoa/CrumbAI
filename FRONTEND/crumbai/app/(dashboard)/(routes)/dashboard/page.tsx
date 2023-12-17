// import Link from 'next/link'
import { getServerSession } from 'next-auth';

const DashboardPage = async () => {
  const session = await getServerSession();

  return (
    <div>
      <p>Dashbaord Page: {session?.user?.name}</p>
    </div>
  );
};

export default DashboardPage;
