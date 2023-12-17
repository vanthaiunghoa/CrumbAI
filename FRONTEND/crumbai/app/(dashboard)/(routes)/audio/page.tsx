"use client";

import { Heading } from "@/components/heading";
import { ImageDown } from "lucide-react";

const AudioPage = () => {
    return (
      <div>
        <Heading 
            title="Audio"
            description="Our most advanced audio generator"
            icon={ImageDown}
            iconColor="#F3B13F"
            bgColor="bg-violet=500/10"
        />
        <div className="px-4 lg:px-8">
            <div>

            </div>
        </div>
      </div>
    );
  };
  
  export default AudioPage;