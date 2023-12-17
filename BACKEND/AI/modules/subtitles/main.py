import os
import whisper


def create_srt(filename):
    print('Creating srt...')
    processed_file = 0
    finished_paths = {}
    model = whisper.load_model("medium.en")

    for i in range(10):
        if os.path.exists(f"tmp/{i}_cropped_{filename}"):
            subtitle_path = f"tmp/{i}_cropped_{filename[:-4]}.srt"
            open(subtitle_path, 'a').close()
            processed_file += 1
            print(f'Processing file {i}_{filename}')

            with open(subtitle_path, 'w') as empty_srt_file:
                pass

            result = model.transcribe(f"tmp/{i}_cropped_{filename[:-4]}.mp4")

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
        if os.path.exists(f"tmp/{i}_cropped_{filename}"):
            processed_file += 1
            print(f'Processing file {i}_cropped_{filename}')
            try:
                font = "force_style='FontName=Londrina Solid,FontSize=20,PrimaryColour=&H00ffffff,OutlineColour=&H00000000," \
                    "BackColour=&H80000000,Bold=1,Italic=0,Alignment=10'"
                sub_format = f"subtitles=tmp/{i}_cropped_{filename[:-4]}.srt:{font}"

                os.system(
                    f'ffmpeg -i tmp/{i}_cropped_{filename} -vf "{sub_format}" -crf 20 -c:v libx264 -b:v 0 -c:a copy tmp/{i}_{filename[:-4]}_subtitled.mp4 -hide_banner -loglevel error')
                print(f'Finished processing file {i}_{filename}')
            except Exception as e:
                print('Error creating subtitles.')
                print(e)
                continue
        else:
            continue



def format_timestamp(seconds, always_include_hours=False):
    if seconds < 0: return None
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
