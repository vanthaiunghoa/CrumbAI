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
                newWidth, newHeight = getNewDimensions(video_stream)


            os.system(f"ffmpeg -i tmp/{i}_{filename} -vf crop={newWidth}:{newHeight} -crf 20 -c:v libx264 -b:v 0 -c:a copy tmp/{i}_cropped_{filename} -hide_banner -loglevel error")
def getNewDimensions(videoStream):
    width = int(videoStream['width'])
    height = int(videoStream['height'])

    if width / height > 9 / 16:  # wider than 9:16, crop sides
        return int(height * (9 / 16)), height
    else:  # narrower than 9:16, crop top and bottom
        return width, int(width * (16 / 9))