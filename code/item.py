
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3 

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left empty")
    
    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if(item): 
            return {
                'message': "success",
                'item': item
            }
        return {
            'message': 'Item not found'
        }, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))     #make to pass comma at last otherwise its not treated as tuple and it should be tuple
        row = result.fetchone()
        connection.close()
        if row:
            return {
                    'item': {
                        'name': row[0],
                        'price': row[1]
                    }
                }
        return None

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'UPDATE items SET price=? WHERE name=?;'
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    def post(self, name):
        item = self.find_by_name(name)
        if(item):
            return {
                'message': "Item already exist."
            }, 400
        data = Item.parser.parse_args()
        try:
            self.insert({'name': name, 'price': data['price']})
            return {
                'message': 'Item created successfully.'
            }, 201
        except:
            return {"message":"An error occured while inserting item"}
        

    def delete(self, name):
        item = self.find_by_name(name)
        if item is None:
            return {
                'message': 'Item does not exist.',
            }
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))     #make to pass comma at last otherwise its not treated as tuple and it should be tuple
        connection.commit()
        connection.close()    
        return {
            'message': 'Item deleted successfully.'
        }, 200

    def put(self, name):
        try: 
            data = Item.parser.parse_args()
            item = self.find_by_name(name)
            if item: 
                self.update({'name': name, 'price': data['price']})
            else: 
                self.insert({'name': name, 'price': data['price']})
            return {'message': 'Item updated successfully.'}
        except:
            return {'message':'Error while updating item'}

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)     #make to pass comma at last otherwise its not treated as tuple and it should be tuple
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()
        return {
            'message': 'Success',
            'data': {
                'item': items
            }
        }
        
