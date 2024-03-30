import { Button } from "./ui/button";

interface VideoClipProps {
  url: string;
  description: string;
}

const VideoClip: React.FC<VideoClipProps> = ({ url, description }) => {
  return (
    <div className="flex flex-col items-center justify-center p-5 shadow-lg bg-[#1e1e1e]">
      <div className="w-full aspect-w-16 aspect-h-9 bg-black">
        <video controls src={url} className="w-full h-full object-contain" />
      </div>
      <p className="text-slate-200 mt-2">{description}</p>
      <Button variant="crumbai" className="mt-5">Upload</Button>
      <Button variant="secondary" className="mt-5">Edit</Button>
      <Button variant="destructive" className="mt-5">Delete</Button>
    </div>
  );
};

export default VideoClip;
