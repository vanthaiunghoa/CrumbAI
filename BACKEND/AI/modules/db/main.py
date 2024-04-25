import os
import mysql.connector
import json
from modules.utils.main import delete_dir, env

class DB:
    """
    Database management class for handling all database interactions.
    Manages video and user status data within a MySQL database.
    """

    def __init__(self, host, user, password, database):
        """
        Initializes the connection to the MySQL database.
        Attempts to connect using provided credentials and outputs the status.
        """
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
        """
        Updates the status of a video processing job in the database.
        """
        query = "UPDATE video_status SET status = %s WHERE unique_id = %s AND user_id = %s"
        values = (status, unique_id, user_id)
        self.cursor.execute(query, values)
        self.mydb.commit()
        print(f'Status updated to {status}.')

    def create_new_video(self, unique_id, user_id, status, settings):
        """
        Inserts a new video entry into the database with initial status and settings.
        """
        query = "INSERT INTO video_status (unique_id, user_id, status, settings) VALUES (%s, %s, %s, %s)"
        values = (unique_id, user_id, status, json.dumps(settings))
        self.cursor.execute(query, values)
        self.mydb.commit()

    def get_status(self, unique_id):
        """
        Retrieves the current status of a video processing job from the database.
        """
        query = "SELECT status FROM video_status WHERE unique_id = %s"
        values = (unique_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        self.mydb.commit()
        return result[0] if result else None

    def save_to_database(self, youtube_url, filename, formatted_content, user_id, unique_id):
        """
        Saves processed video information to the database, including timestamps and descriptions.
        """
        table = [{
            "start_time": content["start_time"],
            "end_time": content["end_time"],
            "description": content["description"],
            "summary": content["summary"],
            "duration": content["duration"],
            "filename": f'{env("SERVER_URL")}/videos/{filename}/{i}_{filename}'
        } for i, content in enumerate(formatted_content)]

        query = "INSERT INTO videos (youtube_url, unique_id, videos, user) VALUES (%s, %s, %s, %s)"
        values = (youtube_url, unique_id, json.dumps(table), user_id)
        self.cursor.execute(query, values)
        self.mydb.commit()

    def save_to_database_existing(self, youtube_url, video_data, user_id, unique_id):
        """
        Saves existing video data to the database.
        """
        query = "INSERT INTO videos (youtube_url, unique_id, videos, user) VALUES (%s, %s, %s, %s)"
        values = (youtube_url, unique_id, video_data, user_id)
        self.cursor.execute(query, values)
        self.mydb.commit()

    def get_existing_data(self, youtube_url, settings):
        """
        Retrieves existing video data from the database.
        """
        query = "SELECT videos FROM videos INNER JOIN video_status ON videos.unique_id = video_status.unique_id WHERE youtube_url = %s AND settings = %s AND video_status.status = 'And we are done!'"
        values = (youtube_url, json.dumps(settings))
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result[0]

    def does_it_exist(self, youtube_url, settings):
        """
        Checks if video data already exists in the database.
        """
        query = "SELECT count(*) FROM videos INNER JOIN video_status ON videos.unique_id = video_status.unique_id WHERE youtube_url = %s AND settings = %s AND video_status.status = 'And we are done!'"
        values = (youtube_url, json.dumps(settings))
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result[0] > 0

    def delete_clip(self, user_id, video_id):
        """
        Deletes a specific video clip from the database.
        """
        query = "DELETE FROM videos WHERE user = %s AND unique_id = %s"
        values = (user_id, video_id)
        self.cursor.execute(query, values)
        self.mydb.commit()

    def get_clips_by_user(self, user_id):
        """
        Retrieves all video clips for a specific user from the database.
        """
        query = "SELECT youtube_url, videos, unique_id, timestamp FROM videos WHERE user = %s ORDER BY timestamp DESC"
        values = (user_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return result

    def get_clip(self, user_id, video_id):
        """
        Retrieves a specific video clip based on user ID and video ID.
        """
        query = "SELECT * FROM videos WHERE user = %s AND video_id = %s ORDER BY timestamp DESC LIMIT 1"
        values = (user_id, video_id)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result

    def delete_old_videos(self):
        """
        Deletes videos older than 2 weeks from the database and associated files from the server.
        """
        query = "SELECT unique_id FROM videos WHERE timestamp < DATE_SUB(NOW(), INTERVAL 2 WEEK)"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for unique_id in result:
            delete_dir(unique_id[0])
            query = "DELETE FROM videos WHERE unique_id = %s"
            values = (unique_id[0],)
            print(f'Deleted video with unique_id: {unique_id[0]}')
            self.cursor.execute(query, values)
            self.mydb.commit()

    def create_tables(self):
        """
        Creates necessary tables if they do not exist already.
        """
        self.cursor.execute("SHOW TABLES LIKE 'videos';")
        result = self.cursor.fetchone()
        if not result:
            create_videos_sql = """
                CREATE TABLE `videos` (
                    `id` int(11) NOT NULL AUTO_INCREMENT,
                    `youtube_url` varchar(128) NOT NULL,
                    `unique_id` varchar(254) NOT NULL,
                    `videos` text NOT NULL,
                    `user` varchar(128) NOT NULL,
                    `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            self.cursor.execute(create_videos_sql)

        # Check and create 'video_status' table
        self.cursor.execute("SHOW TABLES LIKE 'video_status';")
        result = self.cursor.fetchone()
        if not result:
            create_video_status_sql = """
                CREATE TABLE `video_status` (
                    `id` int(11) NOT NULL AUTO_INCREMENT,
                    `unique_id` varchar(128) NOT NULL,
                    `user_id` varchar(128) NOT NULL,
                    `status` varchar(128) NOT NULL,
                    `settings` varchar(1024) NOT NULL,
                    PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            self.cursor.execute(create_video_status_sql)
        self.mydb.commit()

    def close_connection(self):
        """
        Closes the database connection.
        """
        self.cursor.close()
        self.mydb.close()
        print('Connection closed.')
