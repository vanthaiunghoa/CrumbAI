from dotenv import load_dotenv
import os

# Module imports for various functionalities related to video processing
from modules.face_detection.main import master_face_detection
from modules.gameplay.main import add_gameplay
from modules.gpt.main import gpt
from modules.downloader.main import download
from modules.transcribe.main import transcribe
from modules.editing.main import cut_video_up
from modules.db.main import DB
from modules.subtitles.main import master_subtitles
from modules.utils.main import env
from modules.utils.main import move_dir
import json
from rq import Worker, Queue
from redis import Redis

# Print initial startup message
print('Starting Crumb AI...')

# Load environment variables
load_dotenv()

# Database connection initialization
db = DB(env('DB_HOST'), env('DB_USER'), env('DB_PASSWORD'), env('DB_DATABASE'))

# Setup database tables
db.create_tables()

# Initialize GPT model for AI-driven content analysis
open_ai = gpt(env('OPENAI_API_KEY'), env('OPENAI_MODEL'))

if __name__ == '__main__':
    try:
        # Setup Redis worker
        worker = Worker(['default'], connection=Redis(host=env("REDIS_HOST"), port=env("REDIS_PORT"), password=env('REDIS_PASSWORD')))
        worker.work()
    except Exception as e:
        # Handle Redis connection errors
        print('Error connecting to Redis.')
        print(e)

def create(body, job_id):
    """
    Main function to create video content based on input specifications.
    Processes the video by downloading, transcribing, analyzing content,
    editing, detecting faces, adding gameplay features, creating subtitles, and more.
    """
    youtube_url = body['youtube_url']
    user_id = body['user_id']
    settings = body['settings']

    # Check if video data already exists in the database
    if db.does_it_exist(youtube_url, settings):
        videos = db.get_existing_data(youtube_url, settings)
        db.create_new_video(job_id, user_id, 'And we are done! Head to "Your Clips" page to view your video.', settings)
        db.save_to_database_existing(youtube_url, videos, user_id, job_id)
    else:
        # If not exists, proceed with downloading and processing
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

        db.save_to_database(youtube_url, job_id, formatted_content, user_id, job_id)

        # Face detection processing
        if 'face_detection' in settings and settings['face_detection'] == 'true':
            db.set_status(job_id, user_id, 'Detecting faces within the video.')
            master_face_detection(filename)

        # Gameplay feature processing
        if 'gameplay' in settings and settings['gameplay'] and 'enabled' in settings['gameplay'] and settings['gameplay']['enabled'] == 'true':
            db.set_status(job_id, user_id, 'Creating gameplay video.')
            get_type_of_gameplay = settings['gameplay']['type'] or 'random'
            add_gameplay(filename, get_type_of_gameplay)

        # Subtitles processing
        if 'subtitles' in settings and settings['subtitles'] == 'true':
            db.set_status(job_id, user_id, 'Creating subtitles.')
            master_subtitles(filename)

        # Finalising the video
        db.set_status(job_id, user_id, 'Finalising the video.')

        # Move temporary files to permanent storage
        for i in range(0, 10):
            if os.path.exists(f'tmp/{i}_{filename}'):
                move_dir(f'{i}_{filename}', filename[:-4])

        db.set_status(job_id, user_id, 'And we are done! Head to "Your Clips" page to view your video.')
        db.close_connection() # Close database connection
