interface VideoClipProps {
  url: string;
  description: string;
}

const VideoClip: React.FC<VideoClipProps> = ({ url, description }) => {
  return (
    <div className="rounded overflow-hidden shadow-lg w-full h-full object-cover">
      <video controls src={url} className="w-full" />
      <p>{description}</p>
    </div>
  );
};

export default VideoClip;
