import requests

class FoodOrdering:
    def __init__(self):
        self.order_id = 0
        self.menus = {
            "restaurants" : 0,
            "restaurants_data" : [],
        }
        self.registered_restaurants = dict()
        self.restaurant_food_mapper = dict()

    def register_restaurant(self, restaurant_data):
        if restaurant_data["restaurant_id"] not in self.registered_restaurants:
            self.menus["restaurants_data"].append(
                {
                    "name" : restaurant_data["name"],
                    "menu_items" : len(restaurant_data["menu"]),
                    "menu" : restaurant_data["menu"],
                    "rating" : restaurant_data["rating"]
                }
            )
            self.menus["restaurants"] += 1
            self.registered_restaurants[restaurant_data["restaurant_id"]] = restaurant_data
            self.restaurant_food_mapper[restaurant_data["restaurant_id"]] = [
                restaurant_data["menu"][i]["id"] for i in range(len(restaurant_data["menu"]))
            ]

    def distribute_order(self, order):
        general_response = {"order_id" : self.order_id, "orders" : []}
        for i in range(len(order["orders"])):
            if order["orders"][i]["restaurant_id"] in self.registered_restaurants:
                address = self.registered_restaurants[order["orders"][i]["restaurant_id"]]["address"]
                response = requests.get(address + '/v2/order', json = order['orders'][i])
                response["estimated_waiting_time"] = response["cooking_time"]
                del response["cooking_time"]
                general_response["orders"].append(response)
        return general_response
