// import Link from 'next/link'
import { Card, CardContent, CardTitle } from '@/components/ui/card';
import { getServerSession } from 'next-auth';

const DashboardPage = async () => {
  const session = await getServerSession();

  return (
    <div>
      <p>Dashbaord Page: {session?.user?.email}</p>
        <Card>
          <CardTitle>Users</CardTitle>
          <CardContent>100</CardContent>
        </Card>
    </div>
  );
};

export default DashboardPage;
