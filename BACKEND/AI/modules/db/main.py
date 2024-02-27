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
            print('Connected to the database.')
        except Exception as e:
            print('Error connecting to the database.')
            print(e)
    def set_status(self, unique_id, user_id, status):
        query = "UPDATE video_status SET status = %s WHERE unique_id = %s AND user_id = %s"
        values = (status, unique_id, user_id)
        self._execute_query(query, values)

    def create_new_video(self, unique_id, user_id, status, settings):
        query = "INSERT INTO video_status (unique_id, user_id, status, settings) VALUES (%s, %s, %s, %s)"
        values = (unique_id, user_id, status, json.dumps(settings))
        self._execute_query(query, values)

    def get_status(self, unique_id, user_id):
        query = "SELECT status FROM video_status WHERE unique_id = %s AND user_id = %s"
        values = (unique_id, user_id)
        result = self._execute_query(query, values, fetchone=True)
        return result[0] if result else None

    def save_to_database(self, youtube_url, filename, formatted_content):
        table = []
        for i, content in enumerate(formatted_content):
            table.append({
                "start_time": content["start_time"],
                "end_time": content["end_time"],
                "description": content["description"],
                "duration": content["duration"],
                "filename": f'{i}_{filename}'
            })

        query = "INSERT INTO videos (video_url, videos, user) VALUES (%s, %s, %s)"
        values = (youtube_url, json.dumps(table), 'test')
        self._execute_query(query, values)

    def get_existing_data(self, youtube_url, settings):
        query = "SELECT * FROM videos WHERE video_url = %s"
        values = (youtube_url,)
        result = self._execute_query(query, values, fetchone=True)
        if result and result['videos']:
            files = [video['filename'] for video in json.loads(result['videos'])]
            return [file for file in files if not os.path.exists(f'tmp/{file}')]
        return []

    def does_it_exist(self, youtube_url):
        query = "SELECT COUNT(*) FROM videos WHERE video_url = %s"
        values = (youtube_url,)
        result = self._execute_query(query, values, fetchone=True)
        return bool(result[0])

    def get_clips_by_user(self, user_id):
        query = "SELECT * FROM videos WHERE user = %s"
        values = (user_id,)
        result = self._execute_query(query, values, fetchone=True)
        return result[0] if result else None

    def get_clip(self, user_id, video_id):
        query = f"SELECT * FROM videos WHERE user = %s AND video_id = %s"
        values = (user_id, video_id)
        result = self._execute_query(query, values, fetchone=True)
        return result[0] if result else None

    def _execute_query(self, query, values=None, fetchone=False):
        with self.mydb.cursor() as cursor:
            cursor.execute(query, values)
            if fetchone:
                return cursor.fetchone()
            else:
                self.mydb.commit()
