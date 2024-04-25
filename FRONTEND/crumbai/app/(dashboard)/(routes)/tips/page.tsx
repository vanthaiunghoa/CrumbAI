import { Heading } from '@/components/heading';
import { Card, CardContent, CardTitle } from '@/components/ui/card';
import { TrendingUp } from 'lucide-react';

const TipsPage = async () => {
  const tipsAndTrends = [
    {
      title: 'Half Gameplay Shorts',
      "content": "Half Gameplay Shorts provide a visually engaging experience that acts like eye candy for users, enhancing the appeal of their video content. This feature cleverly integrates dynamic gameplay clips into traditional video segments, creating a blend that is both captivating and entertaining. By incorporating interactive gameplay, these shorts not only retain viewer attention longer but also enhance the overall viewing experience. This innovative approach leverages cutting-edge AI technology to analyze and seamlessly integrate relevant gameplay sequences, ensuring that the transitions are smooth and contextually appropriate. The end result is a series of short videos that are not only visually appealing but also uniquely engaging, making them ideal for sharing across social media platforms where capturing the viewer's immediate interest is crucial. Launched on March 30, 2024, this feature has quickly become a favorite among content creators looking to differentiate their offerings and captivate an audience increasingly drawn to interactive and dynamic content.",
      date: 'March 30, 2024',
    },
    {
      "title": 'Generate Engaging Descriptions',
      "content": "Elevate the appeal of your shorts by utilizing CrumbAI's feature to generate engaging descriptions and tags. This AI-driven tool analyzes your video content to craft descriptions that capture the essence and highlights of your shorts, ensuring they resonate with your target audience. These optimized descriptions help improve searchability and engagement by incorporating relevant keywords and phrases that align with viewer searches and interests. Additionally, using the AI to generate smart tags can drastically increase your video’s visibility on platforms like YouTube and TikTok. This tool is not just about automation; it's about enhancing the quality and reach of your content with minimal effort. Take advantage of this feature to ensure your shorts stand out in a competitive content landscape, driving more views and engagements organically. Implement this on your next project, starting April 20, 2024, and watch your digital footprint expand.",
      "date": "April 20, 2024"
    }    
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
