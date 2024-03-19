"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { Heading } from "@/components/heading";
import { Video } from "lucide-react";
import { Button } from "@/components/ui/button";
import { set } from "zod";

const ShortsPage = () => {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [status, setStatus] = useState("");
  const [jobId, setJobId] = useState("");

  const handleUrlChange = (e: {
    target: { value: React.SetStateAction<string> };
  }) => {
    setYoutubeUrl(e.target.value);
  };

  const handleSubmit = async (e: { preventDefault: () => void }) => {
    e.preventDefault();

    const response = await axios.get(`/api/shorts?youtube_url=${youtubeUrl}`);
    setJobId(response.data.job_id);
  };

  const fetchStatus = async () => {
    const statusResponse = await axios.get("/api/status?job_id=" + jobId);
    setStatus(statusResponse.data.status);
  };

  useEffect(() => {
    if (jobId) {
      const interval = setInterval(fetchStatus, 5000);
      return () => clearInterval(interval);
    }
  }, [jobId]);

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
            className="bg-[#232323] lg:col-span-10 border-0 p-3 focus:outline-none"
            placeholder="https://www.youtube.com/watch?v=..."
            value={youtubeUrl}
            onChange={handleUrlChange}
          />
          <Button
            variant="crumbai"
            className="col-span-12 lg:col-span-2 w-full mt-1"
          >
            Generate
          </Button>
        </form>
        {status && (
          <div className="mt-4">
            <h2>Status: {status}</h2>
          </div>
        )}
      </div>
    </div>
  );
};

export default ShortsPage;
