import os

import mysql.connector
import json


class DB:

    def __init__(self, host, user, password, database):
        try:
            self.mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.mydb.cursor()
            print('Connected to the database.')
        except Exception as e:
            print('Error connecting to the database.')
            print(e)

    def set_status(self, unique_id, user_id, status):
        query = "UPDATE video_status SET status = %s WHERE unique_id = %s AND user_id = %s"
        values = (status, unique_id, user_id)
        self.cursor.execute(query, values)
        self.mydb.commit()


    def create_new_video(self, unique_id, user_id, status, settings):
        query = "INSERT INTO video_status (unique_id, user_id, status, settings) VALUES (%s, %s, %s, %s)"
        values = (unique_id, user_id, status, json.dumps(settings))
        self.cursor.execute(query, values)
        self.mydb.commit()

    def get_status(self, unique_id, user_id):
        query = "SELECT status FROM video_status WHERE unique_id = %s AND user_id = %s"
        values = (unique_id, user_id)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result[0] if result else None

    def save_to_database(self, youtube_url, filename, formatted_content, user_id):
        table = []
        for i, content in enumerate(formatted_content):
            table.append({
                "start_time": content["start_time"],
                "end_time": content["end_time"],
                "description": content["description"],
                "duration": content["duration"],
                "filename": f'http://161.97.88.202:8000/videos/{filename}/{i}_{filename}'
            })

        query = "INSERT INTO videos (youtube_url, videos, user) VALUES (%s, %s, %s)"
        values = (youtube_url, json.dumps(table), user_id)
        self.cursor.execute(query, values)
        self.mydb.commit()

    def get_existing_data(self, youtube_url, settings):
        query = "SELECT * FROM videos WHERE youtube_url = %s"
        values = (youtube_url,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()

        if result and result['videos']:
            files = [video['filename'] for video in json.loads(result['videos'])]
            return [file for file in files if not os.path.exists(f'tmp/{file}')]
        return []

    def does_it_exist(self, youtube_url):
        return False # Just for testing
        # query = "SELECT COUNT(*) FROM videos WHERE youtube_url = %s"
        # values = (youtube_url,)
        # self.cursor.execute(query, values)
        # result = self.cursor.fetchone()

        # return result[0] > 0

    def get_clips_by_user(self, user_id):
        query = "SELECT youtube_url, videos FROM videos WHERE user = %s"
        values = (user_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return result

    def get_clip(self, user_id, video_id):
        query = f"SELECT * FROM videos WHERE user = %s AND video_id = %s"
        values = (user_id, video_id)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()

        return result
