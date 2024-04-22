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
        print(f'Status updated to {status}.')


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

    def save_to_database(self, youtube_url, filename, formatted_content, user_id, unique_id):
        table = []
        for i, content in enumerate(formatted_content):
            table.append({
                "start_time": content["start_time"],
                "end_time": content["end_time"],
                "description": content["description"],
                "duration": content["duration"],
                "filename": f'http://194.163.180.166:8000/videos/{filename}/{i}_{filename}'
            })

        query = "INSERT INTO videos (youtube_url, unique_id, videos, user) VALUES (%s, %s, %s, %s)"
        values = (youtube_url, unique_id, json.dumps(table), user_id)
        self.cursor.execute(query, values)
        self.mydb.commit()

    def save_to_database_existing(self, youtube_url, video_data, user_id, unique_id):
        query = "INSERT INTO videos (youtube_url, unique_id, videos, user) VALUES (%s, %s, %s, %s)"
        values = (youtube_url, unique_id, video_data, user_id)
        self.cursor.execute(query, values)
        self.mydb.commit()

    def get_existing_data(self, youtube_url, settings):
        query = "SELECT * FROM videos INNER JOIN video_status ON videos.unique_id = video_status.unique_id WHERE youtube_url = %s AND settings = %s AND video_status.status = 'And we are done!'"
        values = (youtube_url,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result[2]


    def does_it_exist(self, youtube_url, settings):
        query = "SELECT count(*) FROM videos INNER JOIN video_status ON videos.unique_id = video_status.unique_id WHERE youtube_url = %s AND settings = %s AND video_status.status = 'And we are done!'"
        values = (youtube_url, json.dumps(settings))
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        if result[0] > 0:
            return True
        else:
            return False

    def delete_clip(self, user_id, video_id):
        query = "DELETE FROM videos WHERE user = %s AND video_id = %s"
        values = (user_id, video_id)
        self.cursor.execute(query, values)
        self.mydb.commit()

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

    def delete_old_videos(self):
        query = "SELECT unique_id FROM video_status WHERE timestamp < DATE_SUB(NOW(), INTERVAL 2 WEEK)"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for unique_id in result:
            query = "SELECT videos FROM videos WHERE unique_id = %s"
            values = (unique_id[0],)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            videos = json.loads(result[0])
            for video in videos:
                for key, value in video.items():
                    if os.path.exists(f'videos/{value}'):
                        os.remove(f'videos/{value}')
            query = "DELETE FROM videos WHERE unique_id = %s"
            values = (unique_id[0],)
            self.cursor.execute(query, values)
            self.mydb.commit()

    def create_tables(self):
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
            print("Created table `videos`.")

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
            print("Created table `video_status`.")

        self.connection.commit()
        print("Tables created successfully.")

