import sqlite3
from flask_restful import Resource, reqparse

class User:
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
            user = User(row[0], row[1], row[2])
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
            user = User(row[0], row[1], row[2])
        else:
            user = None
        connection.close()
        return user
   
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Username is required.")
    parser.add_argument('password', type=str, required=True, help="Password is required.")

    def post(self):
        data = UserRegister.parser.parse_args()
        if (User.find_by_username(data['username'])):
            return {
                'message': 'User already exists.'
            }
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES(NULL, ?, ?)"

        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()
        return {
            'message': 'User created successfully.'
        }