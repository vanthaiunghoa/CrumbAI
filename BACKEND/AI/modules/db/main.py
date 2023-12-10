import mysql.connector

def connect(dbHost, user, password, database):
    print(f"{dbHost}, {user}, {password}, {database}")
    mydb = mysql.connector.connect(
        host='161.97.88.202',
        user=user,
        password=password,
        database=database
    )
    return mydb