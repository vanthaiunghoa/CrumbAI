from dotenv import load_dotenv
import os

from modules.face_detection.main import crop_video
from modules.gpt.main import gpt
from modules.downloader.main import download
from modules.transcribe.main import transcribe
from modules.editing.main import cut_video_up
from modules.db.main import DB
from modules.subtitles.main import create_srt
from modules.subtitles.main import create_subtitles
from modules.utils.main import env
from modules.utils.main import move_dir
import json
from rq import Worker, Queue
from redis import Redis

print('Starting Crumb AI...')
load_dotenv()
db = DB(env('DB_HOST'), env('DB_USER'), env('DB_PASSWORD'), env('DB_DATABASE'))
open_ai = gpt(env('OPENAI_API_KEY'), env('OPENAI_MODEL'))

if __name__ == '__main__':
    try:
        worker = Worker(['default'], connection=Redis(host="161.97.88.202", port=6379, password="0fRhsy5lHQyDE6qC1mlB"))
        worker.work()
    except Exception as e:
        print('Error connecting to Redis.')
        print(e)

def create(body, job_id):
    youtube_url = body['youtube_url']
    user_id = body['user_id']
    settings = body['settings']
    print(f'Creating video for {youtube_url} with settings {settings}.')
    if db.does_it_exist(youtube_url):
        videos = db.get_existing_data(youtube_url, settings)
    else:
        db.create_new_video(job_id, user_id, 'Video is being downloaded.', settings)
        filename = download(youtube_url, job_id)
        if filename is None:
            db.set_status(user_id, user_id, 'Error downloading the video.')
            return
        db.set_status(job_id, user_id, 'Currently transcribing the video.')
        transcript = transcribe(youtube_url)
        db.set_status(job_id, user_id, 'Analyzing the content.')
        interesting_parts = open_ai.interesting_parts(transcript)
        content = json.loads(interesting_parts)
        formatted_content = content["segments"]
        db.set_status(job_id, user_id, 'Editing the video.')
        cut_video_up(filename, formatted_content)

        print('Saving to database...')
        db.save_to_database(youtube_url, job_id, formatted_content, user_id)
        print('Saved to database.')

        if 'face_detection' in settings and settings['face_detection']:
            db.set_status(job_id, user_id, 'Detecting faces within the video.')
            crop_video(filename)

        if 'subtitles' in settings and settings['subtitles']:
            db.set_status(job_id, user_id, 'Creating subtitles.')
            create_srt(filename)
            create_subtitles(filename)

        if 'gameplay' in settings and settings['gameplay']:
            db.set_status(job_id, user_id, 'Creating gameplay video.')


        db.set_status(job_id, user_id, 'Finalising the video.')

        for i in range(0, 10):
            print(f'Checking if {i}_{filename} exists...')
            if os.path.exists(f'tmp/{i}_{filename[:-4]}.mp4'):
                move_dir(f'{i}_{filename}', filename[:-4])

        db.set_status(job_id, user_id, 'And we are done!')
