
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3 
from modals.item import ItemModal

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left empty")
    parser.add_argument('store_id', type=int, required=True, help="Every item need store id")
    
    @jwt_required()
    def get(self, name):
        item = ItemModal.find_by_name(name)
        if(item): 
            return {
                'message': "success",
                'item': {
                    'name': item.name,
                    'price': item.price,
                    'store': item.store_id,
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
            new_item = ItemModal(name, data['price'], data['store_id'])
            new_item.save_to_db()
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
        item.delete_from_db()
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
                item.store_id = data['store_id']
            else: 
                item = ItemModal(name, data['price'], data['store_id'])
            item.save_to_db()
            return {'message': 'Item updated successfully.', 'data': {
                'item': item.get_json()
            }}
        except:
            return {'message':'Error while updating item'}

class ItemList(Resource):
    def get(self):
        return {
            'message': 'Success',
            'data': {
                'item': [item.get_json() for item in ItemModal.query.all()]
            }
        }
        
