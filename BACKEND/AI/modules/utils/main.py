import os
import uuid


def env(variable):
    """
        Get environment variable.
    """
    return os.getenv(variable)


def create_unique_id():
    """
        Create a unique id for the video.
    """
    return str(uuid.uuid4())


def move_dir(filename, folder):
    """
        Move files to videos folder.
    """
    if not os.path.exists(f'videos/{folder}'):
        os.makedirs(f'videos/{folder}')
    os.system(f'mv tmp/{filename} videos/{folder}/{filename}')

def delete_dir(filename):
    """
        Delete files from tmp folder.
    """
    if os.path.exists(f'videos/{filename}'):
        os.system(f'rm -rf videos/{filename}')
