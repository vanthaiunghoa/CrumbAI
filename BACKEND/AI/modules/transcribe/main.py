from youtube_transcript_api import YouTubeTranscriptApi


def transcribe(video_id):
    """
        Transcribe the video. (via YouTubeTranscriptApi)
    """
    transcript = get_transcript(video_id)
    return format_transcript(transcript)


def get_transcript(video_id):
    """
        Get the transcript of the video using YouTubeTranscriptApi.
    """
    video_id = video_id.split('?v=')[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript


def format_transcript(formatted_transcript):
    """
        Format the transcript to srt format.
    """
    formatted = ''
    for entry in formatted_transcript:
        start_time = "{:.2f}".format(entry['start'])
        end_time = "{:.2f}".format(entry['start'] + entry['duration'])
        text = entry['text']
        formatted += f"{start_time} --> {end_time} : {text}\n"

    return formatted_transcript
