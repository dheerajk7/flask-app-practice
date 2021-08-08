import sqlite3

class UserModel:
    def __init__(self, _id, username, password) -> None:
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))     #make to pass comma at last otherwise its not treated as tuple and it should be tuple
        row = result.fetchone()
        print(row, 'row')
        if row:
            user = UserModel(row[0], row[1], row[2])
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))     #make to pass comma at last otherwise its not treated as tuple and it should be tuple
        row = result.fetchone()
        if row:
            user = UserModel(row[0], row[1], row[2])
        else:
            user = None
        connection.close()
        return user