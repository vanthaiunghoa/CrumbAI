import os
import ffmpeg

def crop_video(filename):
    """
    Crops each video in a temporary directory to a 9:16 aspect ratio if it does not match this ratio already.
    This function is intended for formatting videos for platforms that favor vertical video, such as TikTok or Instagram Stories.
    """
    for i in range(0, 10):
        if os.path.exists(f'tmp/{i}_{filename}'):
            probe = ffmpeg.probe(f'tmp/{i}_{filename}')
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
            width = int(video_stream['width'])
            height = int(video_stream['height'])

            # Check if the video's dimensions are already 9:16
            if width != 9 or height != 16:
                newWidth, newHeight = get_new_dimensions(video_stream)

            # Execute the ffmpeg command to crop the video
            os.system(
                f"ffmpeg -i tmp/{i}_{filename} -vf crop={newWidth}:{newHeight} -crf 5 -c:v libx264 -b:v 0 -c:a copy tmp/{i}_cropped_{filename} -hide_banner -loglevel error")

            # Replace the original file with the cropped version
            os.remove(f'tmp/{i}_{filename}')
            os.rename(f'tmp/{i}_cropped_{filename}', f'tmp/{i}_{filename}')

def get_new_dimensions(video_stream):
    """
    Calculates new dimensions for cropping a video to a 9:16 aspect ratio.
    """
    width = int(video_stream['width'])
    height = int(video_stream['height'])

    if width / height > 9 / 16:  # If the video is wider than 9:16, crop the sides
        return int(height * (9 / 16)), height
    else:  # If the video is narrower than 9:16, crop the top and bottom
        return width, int(width * (16 / 9))

def cut_video_up(filename, interesting_parts):
    """
    Cuts the video into segments based on interesting parts identified, using ffmpeg.
    """
    for i, part in enumerate(interesting_parts):
        start_time = part['start_time']
        end_time = part['end_time']
        duration = part['duration']
        description = part['description']
        cut_video(filename, start_time, end_time, duration, description, i)

def cut_video(filename, start_time, end_time, duration, description, i):
    """
    Helper function to cut a segment from a video file.
    """
    if '.mp4' in filename:
        filename = filename.replace('.mp4', '')
    os.system(
        f"ffmpeg -i tmp/{filename}.mp4 -ss {start_time} -to {end_time} -crf 20 -c:v libx264 -b:v 0 -c:a copy tmp/{i}_{filename}.mp4 -hide_banner -loglevel error")
    return

