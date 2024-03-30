import { Heading } from '@/components/heading';
import { Card, CardContent, CardTitle } from '@/components/ui/card';
import { LayoutDashboard } from 'lucide-react';
import { getServerSession } from 'next-auth';

const DashboardPage = async () => {
  const session = await getServerSession();

  return (
    <div className="space-y-8">
      <Heading
        title="Dashboard"
        description="Welcome to your dashboard"
        icon={LayoutDashboard}
        iconColor="#F3B13F"
        bgColor="bg-violet-500/10"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-5">
        <div className="card bg-[#1e1e1e] rounded-lg shadow-lg p-4 text-white flex items-center justify-between">
          <div>
            <h2 className="card-title font-bold">Estimated Profit ($)</h2>
            <p className="card-content text-lg pt-5">$0</p>
          </div>
          <div className={`flex items-center`}>
            <span className="ml-2"></span>
          </div>
        </div>
        <div className="card bg-[#1e1e1e] rounded-lg shadow-lg p-4 text-white flex items-center justify-between">
          <div>
            <h2 className="card-title font-bold">Total Clips Generated</h2>
            <p className="card-content text-lg pt-5">0</p>
          </div>
          <div className={`flex items-center`}>
            <span className="ml-2"></span>
          </div>
        </div>
        <div className="card bg-[#1e1e1e] rounded-lg shadow-lg p-4 text-white flex items-center justify-between">
          <div>
            <h2 className="card-title font-bold">TikTok Views</h2>
            <p className="card-content text-lg pt-5">0</p>
          </div>
          <div className={`flex items-center`}>
            <span className="ml-2"></span>
          </div>
        </div>
        <div className="card bg-[#1e1e1e] rounded-lg shadow-lg p-4 text-white flex items-center justify-between">
          <div>
            <h2 className="card-title font-bold">Youtube Views</h2>
            <p className="card-content text-lg pt-5">0</p>
          </div>
          <div className={`flex items-center`}>
            <span className="ml-2"></span>
          </div>
        </div>
      </div>

    </div>
  );
};

export default DashboardPage;
