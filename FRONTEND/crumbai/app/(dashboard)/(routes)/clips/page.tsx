"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import VideoClip from "@/components/video-clips";
import { Heading } from "@/components/heading";
import { ListVideo } from "lucide-react";

interface VideoDetail {
  url: string;
}

interface Video {
  video_id: string;
  video_title: string;
  videos: VideoDetail[];
}

const ClipsPage = () => {
  const [videos, setVideos] = useState<Video[]>([]);

  useEffect(() => {
    axios
      .get("/api/clips")
      .then((res) => {
        setVideos(res.data.videos); // Assuming the response has a 'videos' property with the data array
      })
      .catch((err) => {
        console.error("Error fetching clips:", err);
        setVideos([]); // Fallback to an empty array in case of an error
      });
  }, []);

  return (
    <div>
      <Heading
        title="Your Clips"
        description="Here are some clips of your videos"
        icon={ListVideo}
        iconColor="#F3B13F"
        bgColor="bg-violet-500/10"
      />
      {/* Container for the grid */}
      <div className="container mx-auto px-4">
        {/* Grid layout with 3 items per row */}
        <div>
          {videos.map((video) => (
            // Each video group takes up one cell in the grid
            <div key={video.video_id} className="rounded-lg overflow-hidden shadow-lg">
              <h3 className="uppercase pb-2 text-center text-xl font-semibold">{video.video_title}</h3>
              {/* Container for individual video items, if you have multiple per group */}
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-center justify-center">
                {video.videos.map((detail, index) => (
                  // Aspect ratio container for each video
                  <div key={index} className="aspect-w-9 aspect-h-16 w-full">
                    {/* Assuming VideoClip is a functional component rendering the video */}
                    <VideoClip url={detail.url} />
                  </div>
                ))}
              </div>
            </div>
          ))}
            {videos.length === 0 && (
                <div className="text-center italic text-lg font-semibold text-white">
                    You do not have any clips...
                </div>
                )}
        </div>
      </div>
    </div>
  );
  
  
};

export default ClipsPage;
