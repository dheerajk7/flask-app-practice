from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = "my secret"
api = Api(app)

# /auth endpoint is created which will identify on the basis of this function
jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/signup')

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

