from flask import Flask, json, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'My wonderful store',
        'items': [
            {
                'name':'My Item',
                'price': 14.55,
            }
        ]
    }
]

@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': [],
    }
    stores.append(new_store)
    print(stores)
    return jsonify(new_store);

@app.route("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'Store not found.'})

@app.route("/store")
def get_stores():
    return jsonify(stores)

@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price'],
            }
            store['items'].append(new_item)
            return jsonify({
                'message': 'New Item created in store.',
                'item': new_item
            })
    return jsonify({
        'message': 'Store not found.',
    })

@app.route("/store/<string:name>/item")
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)

    return jsonify({
        'message': 'Store not found.'
    })

app.run(port=5000)