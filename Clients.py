import requests
import time
from random import randint, choice
import datetime
from concurrent import futures

class ClientsService:
    def __init__(self, n_clients, min_priority=1, max_priority=3, max_items=5):
        self.n_clients = n_clients
        self.min_priority = min_priority
        self.max_priority = max_priority
        self.max_items = self.max_items

    def get_menu(self, menu):
        self.restaurants = menu["restaurants"]
        self.menu = dict()
        self.prep_time = dict()
        restaurant_id = 0
        for restaurant in menu["restaurant_data"]:
            self.menu[restaurant_id] = [
                restaurant_items["id"] for restaurant_items in restaurant["menu"]
            ]
            self.prep_time[restaurant_id] = {
                restaurant_items["id"] : restaurant_items["preparation-time"] for restaurant_items in restaurant["menu"]
            }
            restaurant_id += 1

    def generate_order(self, order_id):
        n_restaurants = randint(1, self.restaurants)
        orders = []
        for i in range(n_restaurants):
            restaurant = choice(list(self.menu.keys()))
            items = [choice(self.menu[restaurant]) for i in range(self.max_items)]
            priority = randint(self.min_priority, self.max_priority)
            max_wait = max([self.prep_time[restaurant][food] for food in items]) * 1.3
            now = datetime.datetime.now()
            order = {
                "restaurant_id" : restaurant,
                "items" : items,
                "priority" : priority,
                "max_wait" : int(max_wait),
                "created_time": time.mktime(now.timetuple())*1e3
            }
            orders.append(order)
        return {
            "order_id" : order_id,
            "orders" : orders
        }

    def create_orders(self, order_id):
        menu = requests.get('http://172.31.96.44:2000/menu')
        self.get_menu(menu)
        order = self.generate_order(order_id)
        order_response = requests.get('http://172.31.96.44:2000/order', json=order)
        max_time_to_wait = max([order["estimated_waiting_time"] for order in order_response["orders"]])
        time.sleep(int(max_time_to_wait * 1.4))
        result = requests.get(f"http://172.31.96.44:2000/v2/order/{order_id}")
        data = {}
        if "cooking_time" in result:
            if result["cooking_time"] < result['max_wait']:
                data['stars'] = 5
            elif result["cooking_time"] <= result['max_wait'] * 1.1:
                data['stars'] = 4
            elif result["cooking_time"] <= result['max_wait'] * 1.2:
                data['stars'] = 3
            elif result["cooking_time"] <= result['max_wait'] * 1.3:
                data['stars'] = 2
            elif result["cooking_time"] <= result['max_wait'] * 1.4:
                data['stars'] = 1
            else:
                data['stars'] = 0
        else:
            data['stars'] = 0
        requests.post('http://172.31.96.44:2000/post_stars', data)

    def send_orders(self, n_orders):
        with futures.ThreadPoolExecutor as executor:
            to_do = []
            for i in range(n_orders):
                future = executor.submit(self.create_orders, i)
                to_do.append(future)
            for future in futures.as_completed(to_do):
                _ = future.result()