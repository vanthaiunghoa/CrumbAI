import { Heading } from '@/components/heading';
import { Card, CardContent, CardTitle } from '@/components/ui/card';
import { TrendingUp } from 'lucide-react';

const TipsPage = async () => {
  const tipsAndTrends = [
    {
      title: 'Half Gameplay Shorts',
      content: 'This is like eye candy to the users...',
      date: 'March 30, 2024',
    },
    {
      title: 'Reddit Clips',
      content: 'Find interesting reddit posts and convert them to voiceover clips...',
      date: 'April 11, 2024',
    },
  ];

  return (
    <div className="space-y-8">
      <Heading
        title="Tips/Trends"
        description="Any tips or trends we recognise will be displayed here."
        icon={TrendingUp}
        iconColor="#F3B13F"
        bgColor="bg-violet-500/10"
      />

      <div className="flex justify-center">
        <div className="max-w-7xl w-full px-4">
          <div className="grid md:grid-cols-2 lg:grid-cols-2 gap-6">
            {tipsAndTrends.map((tip, index) => (
              <div key={index} className="bg-[#1e1e1e] rounded-lg overflow-hidden shadow-lg">
                <div className="text-xl font-bold text-white p-5">
                  {tip.title}
                </div>
                <div className="text-gray-400 p-5">
                  <p>{tip.content}</p>
                  <div className="text-gray-500 text-sm mt-4">
                    Published on {tip.date}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>



    </div>
  );
};

export default TipsPage;
