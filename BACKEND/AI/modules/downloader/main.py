from pytube import YouTube
import pytube.exceptions

def download(url, filename):
    """
    Downloads a YouTube video at the highest available resolution and saves it as an MP4 file.

    Args:
    url (str): The URL of the YouTube video to download.
    filename (str): The base name for the output file, without file extension.

    Returns:
    str: The path to the downloaded video if successful, or None if an error occurs during download.
    """
    yt = YouTube(url)  # Create a YouTube object using the URL

    try:
        video = yt.streams.filter(file_extension='mp4').get_highest_resolution()  # Select the highest resolution video stream available in MP4 format
        # Attempt to download the video to the specified file within a 'tmp/' directory
        video.download(filename=f'{filename}.mp4', output_path='tmp/')
        return filename + '.mp4'  # Return the full path to the downloaded video file
    # if age restricted video
    except pytube.exceptions.AgeRestrictedError:
        return None
    except:
        # Return None if any error occurs during the download process
        return None
