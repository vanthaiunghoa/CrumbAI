import os
import uuid
def env(variable):
    return os.getenv(variable)

def create_unique_id():
    return format('%s.mp4' % uuid.uuid4()).replace('-', '_')
