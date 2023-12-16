import mysql.connector

def connect(host, user, password, database):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def set_status(mydb, unique_id, user_id, status):
    cursor = mydb.cursor()
    query = f"UPDATE video_status SET status = '{status}' WHERE unique_id = '{unique_id}' AND user_id = '{user_id}'"
    cursor.execute(query)
    mydb.commit()
    cursor.close()

def create_new_video(mydb, unique_id, user_id, status):
    cursor = mydb.cursor()
    query = f"INSERT INTO video_status (unique_id, user_id, status) VALUES ('{unique_id}', '{user_id}', '{status}')"
    cursor.execute(query)
    mydb.commit()
    cursor.close()

def get_status(mydb, unique_id, user_id):
    cursor = mydb.cursor()
    query = f"SELECT status FROM video_status WHERE unique_id = '{unique_id}' AND user_id = '{user_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result[0]