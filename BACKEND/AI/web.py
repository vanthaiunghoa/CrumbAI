from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from rq import Queue
from redis import Redis
import os
import schedule
import time
import threading
from modules.db.main import DB
from modules.utils.main import delete_dir, env
from modules.utils.main import create_unique_id

# Initialize Flask app
app = Flask(__name__)

# Configure Redis queue for background task management
q = Queue(connection=Redis(host=env("REDIS_HOST"), port=env("REDIS_PORT"), password=env("REDIS_PASSWORD")))

# Load environment variables from .env file
load_dotenv()

# Initialize database connection
db = DB(env('DB_HOST'), env('DB_USER'), env('DB_PASSWORD'), env('DB_DATABASE'))

@app.before_request
def bearer_token_check():
    """
    Middleware to check for valid bearer token in the Authorization header.
    Allows requests without tokens only if they are directed to the /videos endpoint.
    """
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

@app.route('/', methods=['GET'])
def index():
    """Returns a simple message indicating the API is operational."""
    return jsonify({'message': 'Crumb AI API'}), 200

@app.route('/create', methods=['POST'])
def create():
    """
    Endpoint to create a video processing job.
    Expects JSON containing 'youtube_url' and 'user_id'.
    """
    body = request.get_json()
    if body is None or not all(k in body for k in ['youtube_url', 'user_id']):
        return jsonify({'error': 'No video_url or user_id provided.'}), 400

    job_id = create_unique_id()
    job = q.enqueue('main.create', job_timeout=3600, args=(body,job_id), job_id=job_id)
    return jsonify({'job_id': job.id}), 200

@app.route('/status', methods=['POST'])
def status():
    """
    Retrieves the status of a video processing job using 'job_id' and 'user_id'.
    """
    body = request.get_json()
    job_id = body.get('job_id')
    user_id = body.get('user_id')
    if not job_id or not user_id:
        return jsonify({'error': 'No job_id or user_id provided.'}), 400
    status = db.get_status(job_id, user_id)

    return jsonify({'status': status}), 200

@app.route('/status-2', methods=['POST'])
def status_2():
    """
    Alternative status check returning job's timeout setting.
    """
    body = request.get_json()
    job_id = body['job_id']
    job = q.fetch_job(job_id)
    if job is None:
        return jsonify({'error': 'No job found.'}), 404
    else:
        return jsonify({'status': job.timeout}), 200

@app.route('/get-clips', methods=['POST'])
def get_clips():
    """
    Retrieves video clips associated with a user_id.
    """
    body = request.get_json()
    user_id = body['user_id']
    if user_id is None:
        return jsonify({'error': 'No user_id provided.'}), 400
    result = db.get_clips_by_user(user_id)

    if result is None:
        return jsonify({'error': 'No videos found.'}), 404
    else:
        return jsonify({'videos': result}), 200

@app.route('/delete', methods=['POST'])
def delete():
    """
    Deletes a specified video clip using 'user_id' and 'video_id'.
    """
    body = request.get_json()
    user_id = body['user_id']
    video_id = body['video_id']
    if not user_id or not video_id:
        return jsonify({'error': 'No user_id or video_id provided.'}), 400
    db.delete_clip(user_id, video_id)
    delete_dir(video_id)
    return jsonify({'message': 'Video deleted.'}), 200

@app.route('/get-clip', methods=['POST'])
def get_clip():
    """
    Retrieves a single video clip based on 'user_id' and 'video_id'.
    """
    body = request.get_json()
    user_id = body['user_id']
    video_id = body['video_id']
    if not user_id or not video_id:
        return jsonify({'error': 'No user_id or video_id provided.'}), 400
    result = db.get_clip(user_id, video_id)

    if result is None:
        return jsonify({'error': 'No video found.'}), 404
    else:
        return jsonify({'video': result[0]}), 200

@app.route('/videos/<path>/<video_id>', methods=['GET'])
def get_video(path, video_id):
    """
    Serves a video file from a specified path and video_id.
    """
    if os.path.exists(f'videos/{path}/{video_id}.mp4'):
        return send_file(f'videos/{path}/{video_id}.mp4')
    else:
        return jsonify({'error': 'Video not found.'}), 404

def run_schedule():
    """
    Background task to execute scheduled tasks every second.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)

def delete_old_videos():
    """
    Scheduled task to delete old videos from the database periodically.
    """
    db.delete_old_videos()
    return

if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=env('SERVER_PORT'), debug=env('FLASK_DEBUG'))
    schedule.every(1).hours.do(delete_old_videos)
    scedule_thread = threading.Thread(target=run_schedule)
    scedule_thread.start()
