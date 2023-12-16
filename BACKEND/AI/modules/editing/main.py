import os
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
    if '.mp4' in filename:
        filename = filename.replace('.mp4', '')
    os.system(f"ffmpeg -i tmp/{filename}.mp4 -ss {start_time} -to {end_time} -crf 20 -c:v libx264 -b:v 0 -c:a copy tmp/{i}_{filename}.mp4 -hide_banner -loglevel error")
    print(f'Video: {i}_{filename} cut. Description: {description}. Duration of cut: {duration} seconds.')
    print('Video cut successfully.')
    return

