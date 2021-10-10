from flask import Flask, request
import json
from Clients import *

clients = ClientsService(10)

app = Flask(__name__)

@app.route('/start')
def start():
    clients.send_orders(20)