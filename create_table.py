import sqlite3
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username text, password text, " \
               "weight INTEGER, age INTEGER, name text) "
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS exercise (id INTEGER PRIMARY KEY, exercise_name text, " \
               "exercise_type text, intensity text, duration INTEGER, source text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY, effort_score INTEGER, username text, " \
               "date datetime) "
cursor.execute(create_table)

connection.commit()
connection.close()
