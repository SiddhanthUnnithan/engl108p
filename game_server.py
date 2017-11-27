"""
    Server for turn-based game.
"""
import uuid
import json

from flask import Flask, jsonify, request
import requests as rq

from utils.client import ClientQueue

# app instance
app = Flask(__name__)

# client specs
cq = ClientQueue()
valid_clients = []

# flags
close_game = {
    'status': False
}

# current game state - last observed cards
game_state = {
    'recently_played': None
}

# misc global variables
json_header = {
    'Content-Type': 'application/json'
}

card_order = [str(num) for num in range(3,11)] + ['J', 'Q', 'K', 'A', '2']
card_deck = sum([[val]*4 for val in card_order], [])


@app.route("/join", method=['POST'])
def join_game():
    if close_game['status']:
        ret_val = {
            'game_status': 'closed'
        }

        return jsonify(ret_val)

    data = request.get_json()
    data = json.loads(data)

    # id corresponds to client IP
    client_id = data['identifier']
    
    valid_clients.append(client_id)

    cq.enq(client_id)

    ret_val = {
        'game_status': 'open'
    }

    rq.post("http://%s:5000/io_route" % client_id, data=json.dumps(ret_val), 
            headers=json_header)

    return True


@app.route("/all_clients", method=['POST'])
def all_clients():
    close_game['status'] = True

    # shuffle cards and send to all clients
    game_open_msg = {
        'message': 'All clients joined. Please await guardian instructions.'
    }

    cd = card_deck

    shuffle(cd)

    allocated_cards = [[] for elem in valid_clients]
    
    client_num = 0

    for card in cd:
        if client_num >= len(valid_clients):
            client_num = 0

        allocated_cards[client_num].append(card)
        
        client_num+=1

    allocated_cards = dict(zip(valid_clients, allocated_cards))

    hand_send = {
        'hand': None
    }

    for client in allocated_cards:
        hand_send['hand'] = allocated_cards[client]
        rq.post("http://%s:5000/post_hand" % client, data=json.dumps(hand_send),
                headers=json_header)

    # shuffle clients and create turn-order
    clients = valid_clients

    shuffle(clients)

    for client in clients:
        cq.enq(client)

    return True
