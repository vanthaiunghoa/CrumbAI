"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import VideoClip from "@/components/video-clips";
import { Heading } from "@/components/heading";
import { ListVideo, Video } from "lucide-react";

interface VideoDetail {
  start_time: number;
  end_time: number;
  description: string;
  duration: number;
  filename: string;
}

interface Video {
  url: string;
  details: VideoDetail[];
}

const ClipsPage = () => {
  const [videos, setVideos] = useState<Video[]>([]);

  useEffect(() => {
    axios
      .get('/api/clips')
      .then((res) => {
        const fetchedVideos: Video[] = res.data.videos.map((video: any) => ({
          url: video[0],
          details: JSON.parse(video[1]),
        }));
        setVideos(fetchedVideos);
      })
      .catch((err) => {
        console.error('Error fetching clips:', err);
        setVideos([]);
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
      <div className="container mx-auto px-4">
      <div>
      {videos.map((video, index) => (
        <div key={index} className="rounded-lg overflow-hidden shadow-lg">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-center justify-center">
            {video.details && video.details.length > 0 ? (
              video.details.map((detail, detailIndex) => (
                <div key={detailIndex} className="aspect-w-9 aspect-h-16 w-full">
                    <VideoClip url={detail.filename} description={detail.description} />
                </div>
              ))
            ) : (
              <div>No details available for video {index}</div>
            )}
          </div>
        </div>
      ))}
        </div>
      </div>
    </div>
  );


};

export default ClipsPage;
