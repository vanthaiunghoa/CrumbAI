from dotenv import load_dotenv
import os

from modules.face_detection.main import crop_video
from modules.gpt.main import gpt
from modules.downloader.main import download
from modules.transcribe.main import transcribe
from modules.editing.main import cut_video_up
from modules.db.main import connect, set_status, create_new_video, get_status
from modules.subtitles.main import create_srt
from modules.subtitles.main import create_subtitles
from modules.utils.main import env
from modules.utils.main import create_unique_id
import json
from rq import Worker, Queue
from redis import Redis

# listen = ['default']
# conn = Redis(host="127.0.0.1", port=6379)
# worker = Worker(map(Queue, listen), connection=conn)

print('Starting Crumb AI...')
load_dotenv()
db = connect(env('DB_HOST'), env('DB_USER'), env('DB_PASSWORD'), env('DB_DATABASE'))
open_ai = gpt(env('OPENAI_API_KEY'), env('OPENAI_MODEL'))


def create(body):
    print('Starting video creation...')
    youtube_url = body['youtube_url']
    user_id = body['user_id']
    settings = body['settings']

    if does_it_exist(youtube_url):
        print('Video already exists in database. Need to return already processed videos.')
        videos = get_existing_data(youtube_url)

    else:
        print('Video does not exist in database. Need to process it.')
        unique_id = create_unique_id()
        create_new_video(db, unique_id, user_id, 'Video is being downloaded.')
        print('Downloading video...')
        filename = download(youtube_url, unique_id)
        if filename is None:
            print('Error downloading video.')
            return
        set_status(db, unique_id, user_id, 'Currently transcribing the video.')
        transcript = transcribe(youtube_url)
        set_status(db, unique_id, user_id, 'Analyzing the content.')
        interesting_parts = open_ai.interesting_parts(transcript)
        content = json.loads(interesting_parts)
        formatted_content = content["segments"]
        set_status(db, unique_id, user_id, 'Editing the video.')
        cut_video_up(filename, formatted_content)

        save_to_database(youtube_url, filename, formatted_content)

        if settings['face_detection']:
            set_status(db, unique_id, user_id, 'Cropping the video.')
            crop_video(filename)

        if settings['subtitles']:
            set_status(db, unique_id, user_id, 'Creating subtitles.')
            create_srt(filename)
            create_subtitles(filename)

        set_status(db, unique_id, user_id, 'And we are done!')


def save_to_database(youtube_url, filename, formatted_content):
    table = {}
    for i in range(len(formatted_content)):
        table[i] = {
            "start_time": formatted_content[i]["start_time"],
            "end_time": formatted_content[i]["end_time"],
            "description": formatted_content[i]["description"],
            "duration": formatted_content[i]["duration"],
            "filename": f'{i}_{filename}'
        }

    cursor = db.cursor()
    query = "INSERT INTO videos (video_url, videos, user) VALUES (%s, %s, %s)"
    values = (youtube_url, json.dumps(table), 'test')
    cursor.execute(query, values)
    db.commit()
    return


def get_existing_data(youtube_url):
    ## todo: return all the data from the database, like how many videos have been processed, etc.
    cursor = db.cursor()
    query = f"SELECT * FROM videos WHERE video_url = '{youtube_url}'"
    cursor.execute(query)
    files = []

    # Get files from drive
    if query['videos'] is not None:
        for video in query['videos']:
            if not os.path.exists(f'tmp/{video.filename}'):
                print('Video does not exist on disk. Need to process it.')
                files.append(video.filename)

    return files


def does_it_exist(youtube_url):
    cursor = db.cursor()
    query = f"SELECT * FROM videos WHERE video_url = '{youtube_url}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    else:
        return True


if __name__ == '__main__':
    #worker.work()
    create({'youtube_url': 'https://www.youtube.com/watch?v=4Y4k0OPO5o0', 'user_id': 'test', 'settings': {'face_detection': False, 'subtitles': False}})