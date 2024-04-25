import clipsai
import os

from modules.utils.main import env

def master_face_detection(filename):
    """
    Processes video files to detect faces and adjusts the video to focus on these faces.
    It uses the clipsai library for video processing tasks such as resizing and cropping based on detected faces.
    """
    media_editor = clipsai.MediaEditor()
    for i in range(0, 10):
        if os.path.exists(f'tmp/{i}_{filename}'):
            path = os.path.abspath(f'tmp/{i}_{filename}')

            # Resize video according to face detection, using the clipsai library
            # Aspect ratio is set to 9:16 which is suitable for platforms like TikTok, Instagram, and YouTube Shorts
            crops = clipsai.resize(
                video_file_path=path,
                pyannote_auth_token=env("HUGGING_FACE_TOKEN"),  # Pyannote for face recognition
                aspect_ratio=(9, 16),  # Maintaining 9:16 aspect ratio for social media suitability
                device="cpu"  # Process on CPU as default computational resource
            )

            new_path = os.path.abspath(f'tmp/{i}_face_detection_{filename}')
            path_formatted = clipsai.AudioVideoFile(path)

            # Using media_editor to apply resizing based on the detected faces and specified dimensions
            media_editor.resize_video(
                original_video_file=path_formatted,
                resized_video_file_path=new_path,
                width=crops.crop_width,
                height=crops.crop_height,
                segments=crops.to_dict()["segments"],  # Segments contain time frames for resizing based on face presence
            )

            # Clean up: remove the original file and replace with the face-detected file
            os.system(f'rm tmp/{i}_{filename}')
            os.system(f'mv tmp/{i}_face_detection_{filename} tmp/{i}_{filename}')
