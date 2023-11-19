from pytube import YouTube
import uuid

def download(url):
    print('Downloading video...')
    yt = YouTube(url)
    video = yt.streams.filter(file_extension='mp4').get_highest_resolution()
    filename = format('%s.mp4' % uuid.uuid4()).replace('-', '_')
    print('Downloading video to %s...' % filename)


    try:
        video.download(filename=filename, output_path='tmp/')
        print('Video downloaded successfully.')
        return filename
    except:
        print('Error downloading video.')
        return None


