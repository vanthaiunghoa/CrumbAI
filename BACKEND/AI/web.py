from flask import Flask, request, jsonify
from rq import Queue
from redis import Redis
import base64
import os
import zipfile

from modules import db
from modules.db.main import get_status

app = Flask(__name__)
redis_connection = Redis(host='127.0.0.1')
q = Queue(connection=redis_connection)

@app.before_request
def bearer_token_check():
    bearer_token = request.headers.get('Authorization')
    if bearer_token is None:
        return jsonify({'error': 'No bearer token provided.'}), 401
    else:
        bearer_token = bearer_token.split(' ')[1]
        if bearer_token != os.getenv('BEARER_TOKEN'):
            return jsonify({'error': 'Invalid bearer token provided.'}), 401
        else:
            return

# /create route
@app.route('/create', methods=['POST'])
def create():
    body = request.get_json()
    if body is None or body.get('video_url') is None:
        return jsonify({'error': 'No video_url provided.'}), 400

    job = q.enqueue('main.create', args=(body,))
    return jsonify({'job_id': job.id}), 200

# /status route
@app.route('/status', methods=['POST'])
def status():
    body = request.get_json()
    job_id = body['job_id']
    job = q.fetch_job(job_id)
    if job is None:
        return jsonify({'error': 'No job found.'}), 404
    else:
        return jsonify({'status': job.get_status()}), 200

@app.route('/status-2', methods=['POST'])
def status_2():
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

if __name__ == '__main__':
    app.run(host='localhost', port=8000)