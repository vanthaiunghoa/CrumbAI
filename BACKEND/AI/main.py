from dotenv import load_dotenv
import os
from modules.gpt.main import gpt
from modules.downloader.main import download
from modules.transcribe.main import transcribe
def main():
    print('Starting Crumb AI...')
    load_dotenv()

    open_ai = gpt(env('OPENAI_API_KEY'), env('OPENAI_MODEL'))

    # Test: passed youtube url
    youtube_url = 'https://www.youtube.com/watch?v=LRMfYOynfGg'

    if does_it_exist(youtube_url):
        print('Video already exists in database. Need to return already processed videos.')
        return
    else:
        print('Video does not exist in database. Need to process it.')
        filename = download(youtube_url)
        transcript = transcribe(youtube_url)
        interesting_parts = open_ai.interesting_parts(transcript)
        print(interesting_parts)




def does_it_exist(youtube_url):
    ## todo: access mysql db and see if the file exists
    return False

def get_existing_data(youtube_url):
    ## todo: return all the data from the database, like how many videos have been processed, etc.
    return None

def env(variable):
    return os.getenv(variable)




if __name__ == '__main__':
    main()