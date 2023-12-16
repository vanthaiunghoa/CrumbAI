import os

def face_dectection_and_crop(filename):
    print('Starting face detection...')
    processed_file = 0

    for i in range(0, 10):
        if os.path.exists(f'tmp/{i}_{filename}'):
            processed_file += 1
            print(f'Processing file {i}_{filename}')

        else:
            print(f'File {i}_{filename} does not exist. Skipping.')
            continue

