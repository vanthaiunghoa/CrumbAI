from dotenv import load_dotenv
import os

from modules.face_detection.main import face_dectection_and_crop
from modules.gpt.main import gpt
from modules.downloader.main import download
from modules.transcribe.main import transcribe
from modules.editing.main import cut_video_up
from modules.db.main import connect
from modules.subtitles.main import create_srt
from modules.subtitles.main import create_subtitles
import json
def main():
    print('Starting Crumb AI...')
    load_dotenv()
    db = connect(env('DB_HOST'), env('DB_USER'), env('DB_PASSWORD'), env('DB_DATABASE'))

    open_ai = gpt(env('OPENAI_API_KEY'), env('OPENAI_MODEL'))

    # Test: passed youtube url
    youtube_url = 'https://www.youtube.com/watch?v=nexAoj8r0ss'

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
        print('Finished cutting video up.')
        print('Saving to database...')
        save_to_database(db, youtube_url, filename, formatted_content)
        #face_dectection_and_crop(filename)
        create_srt(filename)
        create_subtitles(filename)






def does_it_exist(db, youtube_url):
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

def save_to_database(db, youtube_url, filename, formatted_content):
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
    return None

def env(variable):
    return os.getenv(variable)




if __name__ == '__main__':
    main()