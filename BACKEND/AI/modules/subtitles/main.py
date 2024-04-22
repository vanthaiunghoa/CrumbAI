import os
import stable_whisper

def create_srt(filename):
    processed_file = 0
    finished_paths = {}
    model = stable_whisper.load_model("base")

    for i in range(10):
        if os.path.exists(f"tmp/{i}_{filename}"):
            subtitle_path = f"tmp/{i}_{filename[:-4]}.srt"
            open(subtitle_path, 'a').close()
            processed_file += 1

            with open(subtitle_path, 'w') as empty_srt_file:
                pass

            result = model.transcribe(f"tmp/{i}_{filename[:-4]}.mp4")
            result.to_srt_vtt(subtitle_path, segment_level=False, word_level=True, min_dur=0.3)
            formatSubtitles(subtitle_path)

            finished_paths[i] = subtitle_path
        else:
            continue

    return finished_paths


def create_subtitles(filename):
    processed_file = 0

    for i in range(10):
        if os.path.exists(f"tmp/{i}_{filename}"):
            processed_file += 1
            try:
                font_dir = os.path.join(os.path.dirname(__file__), 'fonts')
                font = f"fontsdir={font_dir}:force_style='FontName=Komika Axis,FontSize=15,MarginV=70,PrimaryColour=&H00ffffff,OutlineColour=&H00000000,Outline=2,BorderStyle=1" \
                       "BackColour=&H80000000,Bold=1,Italic=0,Alignment=10'"
                sub_format = f"subtitles=tmp/{i}_{filename[:-4]}.srt:{font}"
                os.system(
                    f'ffmpeg -i tmp/{i}_{filename} -vf "{sub_format}" -crf 20 -c:v libx264 -b:v 0 -c:a copy tmp/{i}_{filename[:-4]}_subtitled.mp4 -hide_banner -loglevel error -y')

                os.system(f'rm tmp/{i}_{filename}')
                os.system(f'mv tmp/{i}_{filename[:-4]}_subtitled.mp4 tmp/{i}_{filename}')
            except Exception as e:
                print('Error creating subtitles.')
                print(e)
                continue
        else:
            continue


def formatSubtitles(subtitle_path):
    with open(subtitle_path, 'r') as file:
        filedata = file.read()
        filedata = filedata.upper()
    with open(subtitle_path, 'w') as file:
        file.write(filedata)

def master_subtitles(filename):
    create_srt(filename)
    create_subtitles(filename)
