import sqlite3
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username text, password text, " \
               "weight INTEGER, age INTEGER, name text) "
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS exercise (id INTEGER PRIMARY KEY, exercise_name text, " \
               "exercise_type text, intensity text, duration INTEGER, source text, description text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY, effort_score INTEGER, username text, " \
               "date Date, exercise_id INTEGER) "
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS exercise_record (id INTEGER PRIMARY KEY, username text, " \
               "date Date, exercise_id INTEGER, user_time INTEGER , total_time INTEGER) "
cursor.execute(create_table)


create_table = "CREATE TABLE IF NOT EXISTS user_data (id INTEGER PRIMARY KEY, username text, " \
               "date Date, weight real) "
cursor.execute(create_table)

connection.commit()
connection.close()
