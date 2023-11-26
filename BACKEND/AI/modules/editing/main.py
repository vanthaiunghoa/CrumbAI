import os
import math
from datetime import datetime
import ffmpeg
## Crop the video
def crop_video():
    return

def cut_video_up(filename, interesting_parts):
    for i, part in enumerate(interesting_parts):
        start_time = part['start_time']
        end_time = part['end_time']
        duration = part['duration']
        description = part['description']
        print(f'Cutting video from {start_time} to {end_time}...')
        cut_video(filename, start_time, end_time, duration, description, i)


def cut_video(filename, start_time, end_time, duration, description, i):
    print('Cutting video...')
    # Small fix for the filename
    if '.mp4' in filename:
        filename = filename.replace('.mp4', '')
    print(start_time)
    os.system(f"ffmpeg -y -hwaccel cuda -i tmp/{filename}.mp4 -crf 5 -b:v 6000k -ss {start_time} -to {end_time} -c copy tmp/{i}_{filename}.mp4 -r 25")
    print(f'Video: {i}_{filename} cut. Description: {description}. Duration of cut: {duration} seconds.')
    print('Video cut successfully.')
    return