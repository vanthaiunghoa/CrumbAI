import os
import subprocess

import cv2 as cv
import ffmpeg

def sub_face_detection(filename):
    detected_faces = []



    return detected_faces

def master_face_detection(filename):
    print('Starting face detection...')
    processed_file = 0
    detected_faces = sub_face_detection(filename)
    print('Finished face detection.')

    try:
        if len(detected_faces) == 0:
            print('No faces detected.')
            return None
        else:
            print('Detecting faces.')

            print('Finished detecting faces.')
    except Exception as e:
        print('Error detecting faces.')
        print(e)
        return None



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


            os.system(f"ffmpeg -i tmp/{i}_{filename} -vf crop={newWidth}:{newHeight} -crf 5 -c:v libx264 -b:v 0 -c:a copy tmp/{i}_cropped_{filename} -hide_banner -loglevel error")
def getNewDimensions(videoStream):
    width = int(videoStream['width'])
    height = int(videoStream['height'])

    if width / height > 9 / 16:  # wider than 9:16, crop sides
        return int(height * (9 / 16)), height
    else:  # narrower than 9:16, crop top and bottom
        return width, int(width * (16 / 9))