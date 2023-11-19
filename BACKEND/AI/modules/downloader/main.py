from pytube import YouTube
import uuid

def download(url):
    print('Downloading video...')
    yt = YouTube(url)
    video = yt.streams.filter(file_extension='mp4').get_highest_resolution()
    filename = format('%s.mp4' % uuid.uuid4())


    try:
        video.download(filename=filename)
        print('Video downloaded successfully.')
        return filename
    except:
        print('Error downloading video.')
        return None


