import os

def face_dectection_and_crop(filename):
    print('Starting face detection...')
    # Check if file exists in the tmp directory
    if not os.path.exists(f'tmp/{filename}.mp4'):
        print('File does not exist in tmp directory. Exiting...')
        return

