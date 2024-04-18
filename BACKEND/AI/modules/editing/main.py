import os
import ffmpeg



def crop_video(filename):
    for i in range(0, 10):
        if os.path.exists(f'tmp/{i}_{filename}'):
            probe = ffmpeg.probe(f'tmp/{i}_{filename}')
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
            width = int(video_stream['width'])
            height = int(video_stream['height'])

            if width != 9 or height != 16:
                newWidth, newHeight = get_new_dimensions(video_stream)

            print(f'Video: {i}_{filename} is {width}x{height}. Cropping to {newWidth}x{newHeight}.')
            os.system(
                f"ffmpeg -i tmp/{i}_{filename} -vf crop={newWidth}:{newHeight} -crf 5 -c:v libx264 -b:v 0 -c:a copy tmp/{i}_cropped_{filename} -hide_banner -loglevel error")

            os.remove(f'tmp/{i}_{filename}')
            os.rename(f'tmp/{i}_cropped_{filename}', f'tmp/{i}_{filename}')



def get_new_dimensions(videoStream):
    width = int(videoStream['width'])
    height = int(videoStream['height'])

    if width / height > 9 / 16:  # wider than 9:16, crop sides
        return int(height * (9 / 16)), height
    else:  # narrower than 9:16, crop top and bottom
        return width, int(width * (16 / 9))

def cut_video_up(filename, interesting_parts):
    for i, part in enumerate(interesting_parts):
        start_time = part['start_time']
        end_time = part['end_time']
        duration = part['duration']
        description = part['description']
        cut_video(filename, start_time, end_time, duration, description, i)


def cut_video(filename, start_time, end_time, duration, description, i):
    if '.mp4' in filename:
        filename = filename.replace('.mp4', '')
    os.system(
        f"ffmpeg -i tmp/{filename}.mp4 -ss {start_time} -to {end_time} -crf 20 -c:v libx264 -b:v 0 -c:a copy tmp/{i}_{filename}.mp4 -hide_banner -loglevel error")
    print(f'Video: {i}_{filename} cut. Description: {description}. Duration of cut: {duration} seconds.')
    return
