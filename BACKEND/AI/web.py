from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from rq import Queue
from redis import Redis
import base64
import os
import json

from modules.db.main import DB
from modules.utils.main import delete_dir, env
from modules.utils.main import create_unique_id

app = Flask(__name__)
q = Queue(connection=Redis(host=env("REDIS_HOST"), port=env("REDIS_PORT"), password=env("REDIS_PASSWORD")))
load_dotenv()
db = DB(env('DB_HOST'), env('DB_USER'), env('DB_PASSWORD'), env('DB_DATABASE'))


@app.before_request
def bearer_token_check():
    if request.path.startswith('/videos'):
        return

    bearer_token = request.headers.get('Authorization')
    if bearer_token is None:
        return jsonify({'error': 'No bearer token provided.'}), 401
    else:
        bearer_token = bearer_token.split(' ')[1]
        if bearer_token != os.getenv('BEARER_TOKEN'):
            return jsonify({'error': 'Invalid bearer token provided.'}), 401
        else:
            return


# / route
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Crumb AI API'}), 200


# /create route
@app.route('/create', methods=['POST'])
def create():
    body = request.get_json()
    if body is None or body.get('youtube_url') is None:
        return jsonify({'error': 'No video_url provided.'}), 400
    if body is None or body.get('user_id') is None:
        return jsonify({'error': 'No user_id provided.'}), 400

    job_id = create_unique_id()
    job = q.enqueue('main.create', job_timeout=2700, args=(body,job_id), job_id=job_id)
    return jsonify({'job_id': job.id}), 200



# /status route
@app.route('/status', methods=['POST'])
def status():
    body = request.get_json()
    job_id = body['job_id']
    user_id = body['user_id']
    if job_id is None or user_id is None:
        return jsonify({'error': 'No job_id or user_id provided.'}), 400
    status = db.get_status(job_id, user_id)

    return jsonify({'status': status}), 200


@app.route('/status-2', methods=['POST'])
def status_2():
    body = request.get_json()
    job_id = body['job_id']
    job = q.fetch_job(job_id)
    if job is None:
        return jsonify({'error': 'No job found.'}), 404
    else:
        return jsonify({'status': job.timeout}), 200


# /get-clips route
@app.route('/get-clips', methods=['POST'])
def get_clips():
    body = request.get_json()
    user_id = body['user_id']
    if user_id is None:
        return jsonify({'error': 'No user_id provided.'}), 400
    result = db.get_clips_by_user(user_id)
    if result is None:
        return jsonify({'error': 'No videos found.'}), 404
    else:
        return jsonify({'videos': result}), 200

# /delete
@app.route('/delete', methods=['POST'])
def delete():
    body = request.get_json()
    user_id = body['user_id']
    video_id = body['video_id']
    if user_id is None or video_id is None:
        return jsonify({'error': 'No user_id or video_id provided.'}), 400
    db.delete_clip(user_id, video_id)
    delete_dir(video_id)
    return jsonify({'message': 'Video deleted.'}), 200

# /get-clip route
@app.route('/get-clip', methods=['POST'])
def get_clip():
    body = request.get_json()
    user_id = body['user_id']
    video_id = body['video_id']
    # Make sure user_id and video_id are provided
    if user_id is None or video_id is None:
        return jsonify({'error': 'No user_id or video_id provided.'}), 400
    # Get clip by user
    result = db.get_clip(user_id, video_id)

    # If no clip found, return 404, else return 200 with the clip
    if result is None:
        return jsonify({'error': 'No video found.'}), 404
    else:
        return jsonify({'video': result[0]}), 200

# /videos/<video_id> route
@app.route('/videos/<path>/<video_id>', methods=['GET'])
def get_video(path, video_id):
    if os.path.exists(f'videos/{path}/{video_id}.mp4'):
        return send_file(f'videos/{path}/{video_id}.mp4')
    else:
        return jsonify({'error': 'Video not found.'}), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
