import { Heading } from "@/components/heading";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LayoutDashboard } from "lucide-react";
import { getServerSession } from "next-auth";

const DashboardPage = async () => {
  const session = await getServerSession();
  const name = session?.user?.name;
  return (
    <div className="space-y-8">
      <Heading
        title="Dashboard"
        description={`Welcome to your dashboard, ${name}!`}
        icon={LayoutDashboard}
        iconColor="#F3B13F"
        bgColor="bg-violet-500/10"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-5">
        <Card className="rounded-lg shadow-lg flex items-center justify-between">
          <CardHeader>
            <CardTitle>
                Estimated Profit ($)
            </CardTitle>
            <CardContent className="text-lg pt-5">$0</CardContent>
          </CardHeader>
        </Card>

        <Card className="rounded-lg shadow-lg flex items-center justify-between">
          <CardHeader>
            <CardTitle>
              Total Clips Generated
            </CardTitle>
            <CardContent className="text-lg pt-5">0</CardContent>
          </CardHeader>
        </Card>

        <Card className="rounded-lg shadow-lg flex items-center justify-between">
          <CardHeader>
            <CardTitle>
              TikTok Views
            </CardTitle>
            <CardContent className="text-lg pt-5">0</CardContent>
          </CardHeader>
        </Card>

        <Card className="rounded-lg shadow-lg flex items-center justify-between">
          <CardHeader>
            <CardTitle>
              YouTube Views
            </CardTitle>
            <CardContent className="text-lg pt-5">0</CardContent>
          </CardHeader>
        </Card>
      </div>

    </div>
  );
};

export default DashboardPage;
