import os
import random
from moviepy.editor import *
from moviepy.video.fx.all import crop

minecraft_gameplay = [
    'MINECRAFT_PARKOUR.mp4',
    'MINECRAFT_PARKOUR_2.mp4',
    'MINECRAFT_PARKOUR_3.mp4',
]

gta_gameplay = [
    'GTA_5_RAMPS.mp4',
    'GTA_5_RAMPS_2.mp4',
]

cluster_gameplay = [
    'CLUSTER_TRUCK.mp4',
]


def add_gameplay(filename, random_video):
    for i in range(0, 10):
        if os.path.exists(f'tmp/{i}_{filename}'):
            found_gameplay = None

            while found_gameplay == None:
                gameplay = get_gameplay(random_video)
                if not os.path.exists(f'footage/{gameplay}'):
                    found_gameplay = gameplay

            tmp_abs_path = os.path.abspath(f'tmp/{i}_{filename}')
            gameplay_abs_path = os.path.abspath(f'modules/gameplay/footage/{found_gameplay}')

            video1 = VideoFileClip(tmp_abs_path)
            video2 = VideoFileClip(gameplay_abs_path)

            start_time = random.uniform(0, max(0, video2.duration - video1.duration))
            end_time = start_time + video1.duration

            end_time = min(end_time, video2.duration)
            video2 = video2.subclip(start_time, end_time)
            video2 = video2.without_audio()

            (w, h) = video1.size
            crop_size = min(w, h)
            bg_video = crop(video1, width=crop_size, height=crop_size, x_center=w/2, y_center=h/2)
            bg_video = bg_video.resize((1080, 960))

            (w, h) = video2.size
            crop_size = min(w, h)
            bg_video2 = crop(video2, width=crop_size, height=crop_size, x_center=w/2, y_center=h/2)
            bg_video2 = bg_video2.resize((1080, 960))
            bg_video2 = bg_video2.set_duration(bg_video.duration)

            video1_pos = (0,0)
            video2_pos = (0,960)

            final_video = CompositeVideoClip([bg_video.set_pos(video1_pos),
                                                bg_video2.set_pos(video2_pos)],
                                                size=(1080, 1920))


            tmp_gameplay_abs_path = os.path.abspath(f'tmp/gameplay_{i}_{filename}')
            final_video.write_videofile(tmp_gameplay_abs_path, fps=30)
            os.system(f'rm tmp/{i}_{filename}')
            os.system(f'mv tmp/gameplay_{i}_{filename} tmp/{i}_{filename}')





def get_gameplay(random_video='random'):
    if random_video == 'minecraft':
        return random.choice(minecraft_gameplay)
    elif random_video == 'gta':
        return random.choice(gta_gameplay)
    elif random_video == 'cluster':
        return random.choice(cluster_gameplay)
    else:
        return random.choice(minecraft_gameplay + gta_gameplay + cluster_gameplay)