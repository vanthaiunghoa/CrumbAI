import clipsai
import os

from modules.utils.main import env



def master_face_detection(filename):
    media_editor = clipsai.MediaEditor()
    for i in range(0, 10):
        if os.path.exists(f'tmp/{i}_{filename}'):
            path = os.path.abspath(f'tmp/{i}_{filename}')

            crops = clipsai.resize(
                video_file_path=path,
                pyannote_auth_token=env("HUGGING_FACE_TOKEN"), # Pyannote for speech recognition
                aspect_ratio=(9, 16), # 9:16 aspect ratio for TikTok/Instagram/YT Shorts
                device="cpu" # Because we are running on a server without a GPU
            )

            new_path = os.path.abspath(f'tmp/{i}_face_detection_{filename}')
            path_formatted = clipsai.AudioVideoFile(path)

            media_editor.resize_video(
                original_video_file=path_formatted,
                resized_video_file_path=new_path,
                width=crops.crop_width,
                height=crops.crop_height,
                segments=crops.to_dict()["segments"],
            )

            os.system(f'rm tmp/{i}_{filename}')
            os.system(f'mv tmp/{i}_face_detection_{filename} tmp/{i}_{filename}')



