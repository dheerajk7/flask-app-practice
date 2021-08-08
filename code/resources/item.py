
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3 
from modals.item import ItemModal


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left empty")
    
    @jwt_required()
    def get(self, name):
        item = ItemModal.find_by_name(name)
        if(item): 
            return {
                'message': "success",
                'item': {
                    'name': item.name,
                    'price': item.price,
                }
            }
        return {
            'message': 'Item not found'
        }, 404

    
    def post(self, name):
        try:
            item = ItemModal.find_by_name(name)
            if(item):
                return {
                    'message': "Item already exist."
                }, 400
            data = Item.parser.parse_args()
            new_item = ItemModal(name, data['price'])
            new_item.insert()
            return {
                'message': 'Item created successfully.'
            }, 201
        except:
            return {"message":"An error occured while inserting item"}
        

    def delete(self, name):
        item = ItemModal.find_by_name(name)
        if item is None:
            return {
                'message': 'Item does not exist.',
            }
        item.delete()
        return {
            'message': 'Item deleted successfully.'
        }, 200

    def put(self, name):
        try: 
            data = Item.parser.parse_args()
            item = ItemModal.find_by_name(name)
            if item: 
                item.name = name
                item.price = data['price']
                item.update()
            else: 
                new_item = ItemModal(name, data['price'])
                new_item.insert()
            return {'message': 'Item updated successfully.'}
        except:
            return {'message':'Error while updating item'}

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items;"
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
        
