"use client";
import React, { useCallback, useEffect, useState } from "react";
import axios from "axios";
import { Heading } from "@/components/heading";
import { Video } from "lucide-react";
import { Button } from "@/components/ui/button";
import { set } from "zod";
import { Checkbox } from "@/components/ui/checkbox"

const ShortsPage = () => {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [faceDetection, setFaceDetection] = useState(false);
  const [subtitles, setSubtitles] = useState(false);
  const [halfGameplay, setHalfGameplay] = useState(false);

  const [status, setStatus] = useState("");
  const [jobId, setJobId] = useState("");

  const handleUrlChange = (e: {
    target: { value: React.SetStateAction<string> };
  }) => {
    setYoutubeUrl(e.target.value);
  };

  const handleFaceDetectionChange = (e: { target: { checked: boolean | ((prevState: boolean) => boolean); }; }) => {
    setFaceDetection(e.target.checked);
  };
  
  const handleSubtitlesChange = (e: { target: { checked: boolean | ((prevState: boolean) => boolean); }; }) => {
    setSubtitles(e.target.checked);
  };
  
  const handleHalfGameplayChange = (e: { target: { checked: boolean | ((prevState: boolean) => boolean); }; }) => {
    setHalfGameplay(e.target.checked);
  };
  

  const handleSubmit = async (e: { preventDefault: () => void }) => {
    e.preventDefault();

    const params = {
      youtube_url: youtubeUrl,
      face_detection: faceDetection,
      subtitles: subtitles,
      half_gameplay: halfGameplay,
    };

    const response = await axios.get(`/api/shorts`, { params });
    setJobId(response.data.job_id);
  };

  const fetchStatus = useCallback(async () => {
    const statusResponse = await axios.get("/api/status?job_id=" + jobId);
    setStatus(statusResponse.data.status);
  }, [jobId]);
  
  useEffect(() => {
    if (jobId) {
      const interval = setInterval(fetchStatus, 5000);
      return () => clearInterval(interval);
    }
  }, [jobId, fetchStatus]);
  

  return (
    <div>
      <Heading
        title="Generate Shorts"
        description="Insert a YouTube URL and let the magic happen!"
        icon={Video}
        iconColor="#F3B13F"
        bgColor="bg-violet-500/10"
      />
      <div className="container mx-auto px-4">
        <form
          onSubmit={handleSubmit}
          className="rounded-lg border-0 bg-[#323232] w-full p-4 px-3 md:px-6 focus-within:shadow-sm grid grid-cols-12 gap-2"
        >
          <input
            type="text"
            className="bg-[#232323] lg:col-span-8 border-0 p-3 focus:outline-none"
            placeholder="https://www.youtube.com/watch?v=..."
            value={youtubeUrl}
            onChange={handleUrlChange}
          />
          <div className="col-span-4 flex justify-start items-center gap-4">
            <div className="flex items-center space-x-2">
              <input
                type="checkbox" 
                id="faceDetection" 
                checked={faceDetection} 
                onChange={handleFaceDetectionChange} 
              />
              <label htmlFor="faceDetection" className="text-sm font-medium">Face Detection</label>
            </div>
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="subtitles"
                checked={subtitles}
                onChange={handleSubtitlesChange}
              />
              <label htmlFor="subtitles" className="text-sm font-medium">Subtitles</label>
            </div>
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="halfGameplay"
                checked={halfGameplay}
                onChange={handleHalfGameplayChange}
              />
              <label htmlFor="halfGameplay" className="text-sm font-medium">Half Gameplay</label>
            </div>
          </div>
          <div className="col-span-12 lg:col-start-6 lg:col-span-2 w-full">
            <Button
              variant="crumbai"
              className="col-span-12 lg:col-span-2 w-full mt-1"
            >
              Generate
            </Button>
          </div>
        </form>
        {status && (
          <div className="mt-4 text-center">
            <h1 className="text-xl text-primary"><b>Status:</b> {status}</h1>
          </div>
        )}
      </div>
    </div>
  );
};

export default ShortsPage;
