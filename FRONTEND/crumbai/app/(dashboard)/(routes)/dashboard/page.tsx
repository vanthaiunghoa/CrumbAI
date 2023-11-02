import Link from 'next/link'
import { Button } from "@/components/ui/button";
import { getServerSession } from 'next-auth';

const DashboardPage = async () => {
  const session = await getServerSession();

  return (
    <>
      <p>Dashboard Page: {session?.user?.email}</p>
      <Link href="/api/auth/signout"><Button>Sign Out</Button></Link>
    </>
  );
};

export default DashboardPage;
