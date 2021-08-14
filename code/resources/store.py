from flask_restful import Resource, reqparse
from sqlalchemy.orm import query
from modals.store import StoreModal

class Store(Resource):
    parser = reqparse.RequestParser()    
    def get(self,name):
        store = StoreModal.find_by_name(name)
        if store:
            return store.get_json() 
        return {'message': 'Store not found.'}, 404

    def post(self, name):
        store = StoreModal.find_by_name(name)
        if store:
            return {'message': 'Store already exists.'}, 400
        store = StoreModal(name)
        try:
            store.save_to_db()
        except: 
            return {'message': 'Internal server error'}, 500
        return store.get_json(), 201

    def delete(self, name):
        store = StoreModal.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store delete successfully.'}
        return {'message': 'Error while deleting store.'}


class StoreList(Resource):
    
    def get(self):
        return {
            'message': 'Stores fetched successfully.',
            'data': [store.get_json() for store in StoreModal.query.all()]
        }