from dotenv import load_dotenv
import os

from modules.face_detection.main import face_dectection_and_crop
from modules.gpt.main import gpt
from modules.downloader.main import download
from modules.transcribe.main import transcribe
from modules.editing.main import cut_video_up
from modules.db.main import connect
import json
def main():
    print('Starting Crumb AI...')
    load_dotenv()
    db = connect(env('DB_HOST'), env('DB_USER'), env('DB_PASSWORD'), env('DB_DATABASE'))

    open_ai = gpt(env('OPENAI_API_KEY'), env('OPENAI_MODEL'))

    # Test: passed youtube url
    youtube_url = 'https://www.youtube.com/watch?v=h_SMkjLvT9g'

    if does_it_exist(db, youtube_url):
        print('Video already exists in database. Need to return already processed videos.')
        return
    else:
        print('Video does not exist in database. Need to process it.')
        filename = download(youtube_url)
        if filename is None:
            print('Error downloading video.')
            return
        transcript = transcribe(youtube_url)
        interesting_parts = open_ai.interesting_parts(transcript)
        print('Received interesting parts from GPT')
        content = json.loads(interesting_parts)
        formatted_content = content["segments"]
        print(formatted_content)
        cut_video_up(filename, formatted_content)
        face_dectection_and_crop(filename)







def does_it_exist(db, youtube_url):
    cursor = db.cursor()
    query = f"SELECT * FROM videos WHERE video_url = '{youtube_url}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    else:
        # Get videos from the table
        videos = result[0].videos
        # Check if they exist on the disk
        for video in videos:
            if not os.path.exists(f'tmp/{video}.mp4'):
                print('Video does not exist on disk. Need to process it.')
                return False

        return videos

def get_existing_data(youtube_url):
    ## todo: return all the data from the database, like how many videos have been processed, etc.
    return None

def env(variable):
    return os.getenv(variable)




if __name__ == '__main__':
    main()