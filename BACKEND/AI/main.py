from dotenv import load_dotenv
import os

from flask import Flask, request, jsonify
from rq import Queue
from redis import Redis
import base64

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


## Init API, Redis, and RQ
app = Flask(__name__)
redis_connection = Redis(host='redis')
q = Queue(connection=redis_connection)

print('Starting Crumb AI...')
load_dotenv()
db = connect(env('DB_HOST'), env('DB_USER'), env('DB_PASSWORD'), env('DB_DATABASE'))
open_ai = gpt(env('OPENAI_API_KEY'), env('OPENAI_MODEL'))


# Bearer Token Check
@app.before_request
def bearer_token_check():
    bearer_token = request.headers.get('Authorization')
    if bearer_token is None:
        return jsonify({'error': 'No bearer token provided.'}), 401
    else:
        if bearer_token != os.getenv('BEARER_TOKEN'):
            return jsonify({'error': 'Invalid bearer token provided.'}), 401
        else:
            return


## /create route
@app.route('/create', methods=['POST'])
def create():
    # Get youtube url from body, and user id
    body = request.get_json()
    youtube_url = body['youtube_url']
    user_id = body['user_id']
    settings = body['settings']

    if does_it_exist(youtube_url):
        print('Video already exists in database. Need to return already processed videos.')
        videos = get_existing_data(youtube_url)
        ## test return for now
        return jsonify({'videos': videos}), 200
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


# status route
@app.route('/status', methods=['POST'])
def status():
    body = request.get_json()
    unique_id = body['unique_id']
    user_id = body['user_id']
    status = get_status(db, unique_id, user_id)

    return jsonify({'status': status}), 200

# /get-clips route
@app.route('/get-clips', methods=['POST'])
def get_clips():
    body = request.get_json()
    user_id = body['user_id']

    cursor = db.cursor()
    query = f"SELECT * FROM videos WHERE user = '{user_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return jsonify({'error': 'No videos found.'}), 404
    else:
        return jsonify({'videos': result[0]}), 200

# /get-clip route
@app.route('/get-clip', methods=['POST'])
def get_clip():
    body = request.get_json()
    user_id = body['user_id']
    video_id = body['video_id']

    cursor = db.cursor()
    query = f"SELECT * FROM videos WHERE user = '{user_id}' AND video_id = '{video_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return jsonify({'error': 'No video found.'}), 404
    else:
        return jsonify({'video': result[0]}), 200

def does_it_exist(youtube_url):
    cursor = db.cursor()
    query = f"SELECT * FROM videos WHERE video_url = '{youtube_url}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    else:
        videos = result[0].videos
        for video in videos:
            if not os.path.exists(f'tmp/{video.filename}'):
                print('Video does not exist on disk. Need to process it.')
                return False

        return True

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


if __name__ == '__main__':
    app.run(host='0.0.0.0')