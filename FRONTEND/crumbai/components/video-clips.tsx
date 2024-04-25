import { Button } from "./ui/button";

interface VideoClipProps {
  url: string;
  description: string;
  start?: number;
  end?: number;
}

const VideoClip: React.FC<VideoClipProps> = ({ url, description, start, end }) => {
  var startString = "0:00";
  var endString = "0:00";

  if (start) {
    const startMinutes = Math.floor(start / 60);
    const startSeconds = Math.round(start % 60);
    startString = `${startMinutes}:${startSeconds < 10 ? `0${startSeconds}` : startSeconds}`;
  }

  if (end) {
    const endMinutes = Math.floor(end / 60);
    const endSeconds = Math.round(end % 60);
    endString = `${endMinutes}:${endSeconds < 10 ? `0${endSeconds}` : endSeconds}`;
  }

  return (
    <div className="flex flex-col items-center justify-center p-5">
      <div className="w-full aspect-w-16 aspect-h-9 bg-black mb-2">
        <video controls src={url} className="w-full h-full object-contain" />
      </div>
      <p><b>Start Time:</b> {startString}</p>
      <p><b>End Time:</b> {endString}</p>
      <p className="text-slate-200 mt-2 text-center">{description}</p>
    </div>
  );
};

export default VideoClip;
