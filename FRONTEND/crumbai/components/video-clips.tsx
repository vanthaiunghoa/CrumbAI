const VideoClip = ({ url }: { url: string }) => {
  return (
    <div className="rounded overflow-hidden shadow-lg w-full h-full object-cover">
      <video controls src={url} className="w-full" />
    </div>
  );
};

export default VideoClip;