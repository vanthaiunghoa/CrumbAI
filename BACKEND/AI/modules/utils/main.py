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
    print(f'{folder}')
    # create folder
    if not os.path.exists(f'videos/{folder}'):
        os.makedirs(f'videos/{folder}')
    os.system(f'mv tmp/{filename} videos/{folder}/{filename}')
    print('Files moved successfully.')

def delete_dir(filename):
    """
        Delete files from tmp folder.
    """
    os.system(f'rm tmp/{filename}')
    print('Files deleted successfully.')