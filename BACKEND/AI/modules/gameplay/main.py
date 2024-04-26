import os
import random
from moviepy.editor import *
from moviepy.video.fx.all import crop

# Lists of available gameplay footage files for different games
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
    """
    Integrates gameplay video with an existing video file.
    This function selects gameplay footage based on the given 'random_video' category,
    composites it with the target video, and saves the result.
    """
    for i in range(0, 10):
        if os.path.exists(f'tmp/{i}_{filename}'):
            found_gameplay = None

            # Find a gameplay video that actually exists in the directory
            while found_gameplay is None:
                gameplay = get_gameplay(random_video)
                if os.path.exists(f'modules/gameplay/footage/{gameplay}'):
                    found_gameplay = gameplay

            tmp_abs_path = os.path.abspath(f'tmp/{i}_{filename}')
            gameplay_abs_path = os.path.abspath(f'modules/gameplay/footage/{found_gameplay}')

            video1 = VideoFileClip(tmp_abs_path)
            video2 = VideoFileClip(gameplay_abs_path)

            # Calculate subclip timings for the gameplay to match video1 duration
            start_time = random.uniform(0, max(0, video2.duration - video1.duration))
            end_time = start_time + video1.duration

            video2 = video2.subclip(start_time, end_time)
            video2 = video2.without_audio()  # Remove audio to focus on visual composite

            # Crop and resize video1 to fit within a specific frame
            (w, h) = video1.size
            crop_size = min(w, h)
            bg_video = crop(video1, width=crop_size, height=crop_size, x_center=w/2, y_center=h/2)
            bg_video = bg_video.resize((1080, 960))

            # Crop and resize video2 similarly
            (w, h) = video2.size
            crop_size = min(w, h)
            bg_video2 = crop(video2, width=crop_size, height=crop_size, x_center=w/2, y_center=h/2)
            bg_video2 = bg_video2.resize((1080, 960))
            bg_video2 = bg_video2.set_duration(bg_video.duration)

            # Position videos within a final composite frame
            video1_pos = (0, 0)
            video2_pos = (0, 960)

            final_video = CompositeVideoClip([bg_video.set_pos(video1_pos),
                                              bg_video2.set_pos(video2_pos)],
                                             size=(1080, 1920))

            # Save the composited video and replace the original
            tmp_gameplay_abs_path = os.path.abspath(f'tmp/gameplay_{i}_{filename}')
            final_video.write_videofile(tmp_gameplay_abs_path, fps=30)
            os.system(f'rm tmp/{i}_{filename}')
            os.system(f'mv tmp/gameplay_{i}_{filename} tmp/{i}_{filename}')

def get_gameplay(random_video='random'):
    """
    Selects a gameplay video file randomly from the predefined lists based on the game type.
    """
    if random_video == 'minecraft':
        return random.choice(minecraft_gameplay)
    elif random_video == 'gta':
        return random.choice(gta_gameplay)
    elif random_video == 'cluster':
        return random.choice(cluster_gameplay)
    else:
        # Default to choosing from any gameplay if not specified
        return random.choice(minecraft_gameplay + gta_gameplay + cluster_gameplay)
