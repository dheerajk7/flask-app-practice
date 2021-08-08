import sqlite3

class ItemModal:
    def __init__(self, name, price) -> None:
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))     #make to pass comma at last otherwise its not treated as tuple and it should be tuple
        row = result.fetchone()
        connection.close()
        if row:
            return cls(row[0], row[1])
        return None

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(?, ?)"
        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'UPDATE items SET price=? WHERE name=?;'
        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()

    def delete(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (self.name,))
        connection.commit()
        connection.close()

