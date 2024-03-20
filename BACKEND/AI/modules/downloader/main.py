from pytube import YouTube


def download(url, filename):
    yt = YouTube(url)
    video = yt.streams.filter(file_extension='mp4').get_highest_resolution()

    try:
        video.download(filename=f'{filename}.mp4', output_path='tmp/')
        return filename + '.mp4'
    except:
        return None
