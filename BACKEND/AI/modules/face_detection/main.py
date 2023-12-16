import os
import cv2 as cv
import ffmpeg

def detect_amt_of_faces(video_file):
    detected_faces = []
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
    video_capture = cv.VideoCapture(video_file)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        detected_faces.append(len(faces))

    video_capture.release()
    cv.destroyAllWindows()

    return detected_faces

def sub_face_detection(filename):
    processed_file = 0
    detected_faces = []
    for i in range(0, 10):
        if os.path.exists(f'tmp/{i}_{filename}'):
            processed_file += 1
            print(f'Processing file {i}_{filename}')
            result = detect_amt_of_faces(f'tmp/{i}_{filename}')
            detected_faces.append(result)
        else:
            print(f'File {i}_{filename} does not exist. Skipping.')
            continue


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
            for i in range(0, 10):
                if os.path.exists(f'tmp/{i}_{filename}'):
                    processed_file += 1
                    print(f'Processing file {i}_{filename}')

                    video_capture = cv.VideoCapture(f'{i}_{filename}')
                    frame_width = int(video_capture.get(cv.CAP_PROP_FRAME_WIDTH))
                    frame_height = int(video_capture.get(cv.CAP_PROP_FRAME_HEIGHT))

                    target_height = int(frame_height * 0.8)
                    target_width = int(frame_width * 9/ 16)

                    video_writer = cv.VideoWriter_fourcc(*'mp4v')
                    out = cv.VideoWriter(f'tmp/{i}_cropped_{filename}', video_writer, 20.0, (target_width, target_height))

                    while True:
                        ret, frame = video_capture.read()
                        if not ret:
                            break
                        for detected_face in detected_faces:
                            x, y, w, h = detected_face

                            # Crop the frame
                            crop_x = max(0, x + (w - target_width) // 2)
                            crop_y = max(0, y + (h - target_height) // 2)
                            crop_x2 = min(crop_x + target_width, frame_width)
                            crop_y2 = min(crop_y + target_height, frame_height)

                            frame = frame[crop_y:crop_y2, crop_x:crop_x2]

                            # Resize the frame
                            frame = cv.resize(frame, (target_width, target_height))

                            # Write the frame
                            out.write(frame)

                    video_capture.release()
                    out.release()
                else:
                    print(f'File {i}_{filename} does not exist. Skipping.')
                    continue

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
            width = int(video_stream['width'])
            height = int(video_stream['height'])

            if width != 9 or height != 16:
                newWidth, newHeight = getNewDimensions(video_stream)

                # Crop the video
                ffmpeg.input(f'tmp/{i}_{filename}').filter('crop', newWidth, newHeight).output(f'tmp/{i}_cropped_{filename}').run()

def getNewDimensions(videoStream):
    width = int(videoStream['width'])
    height = int(videoStream['height'])

    if width / height > 9 / 16:  # wider than 9:16, crop sides
        return int(height * (9 / 16)), height
    else:  # narrower than 9:16, crop top and bottom
        return width, int(width * (16 / 9))