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
  unique_id: string;
  timestamp: string;
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
          unique_id: video[2],
          timestamp: video[3],
        }));
        setVideos(fetchedVideos);
      })
      .catch((err) => {
        console.error('Error fetching clips:', err);
        setVideos([]);
      });
  }, []);

  const deleteVideo = (unique_id: string) => {
    axios.get(`/api/clips_delete?unique_id=${unique_id}`)
      .then(() => {
        // Remove the video from the state to update the UI
        setVideos(prevVideos => prevVideos.filter(video => video.unique_id !== unique_id));
      })
      .catch(err => {
        console.error('Error deleting video:', err);
      });
  };

  return (
    <div>
      <Heading
        title="Your Clips"
        description="Here are short clips generated from your videos"
        icon={ListVideo}
        iconColor="#F3B13F"
        bgColor="bg-violet-500/10"
      />
      <div className="container mx-auto px-4 py-8">
      <div>
      {videos.map((video, index) => (
          <div key={index} className="bg-[#1e1e1e] p-10 rounded-lg overflow-hidden mb-8">
          <p className="text-center"><b>Original Video: </b><a target="_blank" href={video.url}>{video.url}</a></p>
          <p className="text-center text-slate-200 mt-2"><i>{video.timestamp}</i></p>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2 mt-2">
            {video.details && video.details.length > 0 ? (
              video.details.map((detail, detailIndex) => (
                <VideoClip key={detailIndex} url={detail.filename} description={detail.description} start={detail.start_time} end={detail.end_time} />
              ))
            ) : (
              <div className="col-span-full text-center text-white">No details available for video {index}</div>
            )}
          </div>
          <div className="text-center">
          <button onClick={() => deleteVideo(video.unique_id)} className="mt-2 py-2 px-4 bg-red-500 hover:bg-red-700 text-white font-bold rounded">
            Delete Videos
          </button>
          </div>
        </div>
      ))}
        </div>
      </div>
    </div>
  );


};

export default ClipsPage;
