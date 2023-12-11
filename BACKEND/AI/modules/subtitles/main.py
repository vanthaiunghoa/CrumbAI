import os
import whisper
from typing import Iterator, TextIO
import ffmpeg # test for subtitles


def create_srt(filename):
    print('Creating srt...')
    processed_file = 0
    finished_paths = {}
    model = whisper.load_model("small")

    for i in range(10):
        if os.path.exists(f"tmp/{i}_{filename}"):
            subtitle_path = f"tmp/{i}_{filename[:-4]}.srt"
            # create empty srt file
            open(subtitle_path, 'a').close()
            processed_file += 1
            print(f'Processing file {i}_{filename}')

            # Ensure SRT file exists and is empty
            with open(subtitle_path, 'w') as empty_srt_file:
                pass

            # Remove .mp4 from original filename
            original_filename = filename[:-4]
            srt_file = f"tmp/{i}_{original_filename}.srt"

            result = model.transcribe(f"tmp/{i}_{original_filename}.mp4")

            with open(subtitle_path, "w") as srt_file_writer:
                write_srt(result["segments"], file=srt_file_writer)

            finished_paths[i] = subtitle_path
        else:
            continue

    return finished_paths

def create_subtitles(filename):
    print('Creating subtitles...')
    processed_file = 0

    for i in range(10):
        if os.path.exists(f"tmp/{i}_{filename}"):
            processed_file += 1
            print(f'Processing file {i}_{filename}')
            try:
                font = "force_style='Alignment=2,MarginV=40,MarginL=55,MarginR=55,Fontname=Noto Sans,Fontsize=11,PrimaryColour=\\&H00d7ff\\&,Outline=1,Shadow=1,BorderStyle=1'"
                sub_format = f"subtitles=tmp/{i}_{filename[:-4]}.srt:{font}"

                os.system(
                    f'ffmpeg -i tmp/{i}_{filename} -vf "{sub_format}" tmp/{i}_{filename[:-4]}_subtitled.mp4 -hide_banner -loglevel error')

            except Exception as e:
                print('Error creating subtitles.')
                print(e)
                continue
        else:
            continue



def format_timestamp(seconds, always_include_hours=False):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)
    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000
    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000
    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000
    hours_marker = f"{hours}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def write_srt(transcript, file):
    for i, segment in enumerate(transcript, start=1):
        file.write(f"{i}\n"
                    f"{format_timestamp(segment['start'], always_include_hours=True)} --> "
                    f"{format_timestamp(segment['end'], always_include_hours=True)}\n"
                    f"{segment['text'].strip().replace('-->', '->')}\n\n")
