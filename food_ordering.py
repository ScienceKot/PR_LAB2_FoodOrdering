from flask import Flask, request, jsonify
import json
import requests
from FoodOrdering import FoodOrdering
food_ordering = FoodOrdering()
app = Flask(__name__)

@app.route('/register', methods=["GET", "POST"])
def register():
    restaurant = request.json
    restaurant['address'] = request.base_url
    food_ordering.register_restaurant(restaurant)
    return "nothing"

@app.route('/order', methods=["GET"])
def order():
    orders = request.json
    general_orders = food_ordering.distribute_order(orders)
    return jsonify(general_orders)

@app.route('/menu', methods=["GET"])
def menu():
    return jsonify(food_ordering.menus)

@app.route('/post_stars', methods=["POST"])
def post_stars():
    data = request.json
    print(data['stars'])

