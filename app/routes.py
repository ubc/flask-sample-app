# app/routes.py
import os
from app import app
from flask import request

items = []

@app.route('/')
def hello():
    app_name = os.getenv("APP_NAME", "Test")
    return f"Hello, {app_name}!"
   # return "Hello, Flask!"

@app.route('/items', methods=['GET'])
def get_items():
    return {'items': items}

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    if item_id < len(items):
        return {'item': items[item_id]}
    else:
        return {'error': 'Item not found'}, 404

@app.route('/items', methods=['POST'])
def add_item():
    item = request.get_json()
    items.append(item)
    return {'message': 'Item added successfully'}, 201
