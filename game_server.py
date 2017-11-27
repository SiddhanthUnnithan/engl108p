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
            'message': 'Game is closed. Check with guardian about next round.'
        }

        return jsonify(ret_val)

    data = request.get_json()
    data = json.loads(data)

    # id corresponds to client IP
    client_id = data['identifier']
    
    valid_clients.append(client_id)

    cq.enq(client_id)

    ret_val = {
        'message': 'Successfully joined game. Status: OPEN.'
    }

    return jsonify(ret_val)


@app.route("/all_clients", method=['POST'])
def all_clients():
    close_game['status'] = True

    # send game open message to all clients
    game_open_msg = {
        'message': 'All clients joined. Please await guardian instructions.'
    }
    
    for client_id in valid_clients:
        rq.post("http://%s:8080/io_route" % client_id, 
                data=json.dumps(game_open_msg), headers=json_header)

    # shuffle cards and send to all clients
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
        rq.post("http://%s:8080/post_hand" % client, data=json.dumps(hand_send),
                headers=json_header)

    # shuffle clients and create turn-order
    clients = valid_clients

    shuffle(clients)

    for client in clients:
        cq.enq(client)

    return True


if __name__ == '__main__':
    # instantiate app server
    app.run(host="0.0.0.0", port=8080, debug=True)
