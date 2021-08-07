from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "my secret"
api = Api(app)

# /auth endpoint is created which will identify on the basis of this function
jwt = JWT(app, authenticate, identity)

items = [
    {
        'name':'Old Item',
        'price': 12.22
    }
]

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left empty")
    
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is not None:
            return {
                'message': 'Success',
                'data': {
                    'item': item
                }
            }
        return {
            'message': 'Item not found'
        }, 404

    def post(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is not None: 
            return {
                'message': 'Item with name {} already exist'.format(name)
            }, 400
        # request_data = request.get_json(force=True)     #when content type header is not sent
        # request_data = request.get_json(silent=True)     #it will return none when nothing found.
        request_data = Item.parser.parse_args()
        new_item = {'name': name, 'price': request_data['price']}
        items.append(new_item)
        return {
            'message': 'Item Created',
            'data': {
                'item': new_item
            }
        }, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {
            'message': "Item deleted."
        }

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            new_item = { 'name': name, 'price': data['price']}
            item = new_item
            items.append(new_item)
        else:
            item.update(data)
        return {
            'message': 'Item Updated.',
            'item': item
        }
class ItemList(Resource):
    def get(self):
        return {
            'message': 'Success',
            'data': {
                'item': items
            }
        }
        

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)

# stores = [
#     {
#         'name': 'My wonderful store',
#         'items': [
#             {
#                 'name':'My Item',
#                 'price': 14.55,
#             }
#         ]
#     }
# ]

# @app.route("/store", methods=["POST"])
# def create_store():
#     request_data = request.get_json()
#     new_store = {
#         'name': request_data['name'],
#         'items': [],
#     }
#     stores.append(new_store)
#     print(stores)
#     return jsonify(new_store);

# @app.route("/store/<string:name>")
# def get_store(name):
#     for store in stores:
#         if store['name'] == name:
#             return jsonify(store)
#     return jsonify({'message': 'Store not found.'})

# @app.route("/store")
# def get_stores():
#     return jsonify(stores)

# @app.route("/store/<string:name>/item", methods=["POST"])
# def create_item_in_store(name):
#     request_data = request.get_json()
#     for store in stores:
#         if store['name'] == name:
#             new_item = {
#                 'name': request_data['name'],
#                 'price': request_data['price'],
#             }
#             store['items'].append(new_item)
#             return jsonify({
#                 'message': 'New Item created in store.',
#                 'item': new_item
#             })
#     return jsonify({
#         'message': 'Store not found.',
#     })

# @app.route("/store/<string:name>/item")
# def get_items_in_store(name):
#     for store in stores:
#         if store['name'] == name:
#             return jsonify(store)

#     return jsonify({
#         'message': 'Store not found.'
#     })

