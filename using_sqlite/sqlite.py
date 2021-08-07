import sqlite3
from sqlite3.dbapi2 import connect

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE users(id int, username text, password text)"

cursor.execute(create_table)

# To insert one user
user = (1, 'jose', '1234')
insert_query = "INSERT INTO users VALUES(?, ?, ?)"
cursor.execute(insert_query, user)

# TO inser many user
users = [
    (2, 'rolf', '1234'),
    (3, 'abc','123')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * from users"

for row in cursor.execute(select_query):
    print(row)
connection.commit()
connection.close()