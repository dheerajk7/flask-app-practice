import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(query)

query = "CREATE TABLE IF NOT EXISTS items(name text, price real)"
cursor.execute(query)

query = "INSERT INTO items VALUES('test', 12.00)"
cursor.execute(query)

connection.commit()
connection.close()