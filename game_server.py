"""
    Server for turn-based game.
"""
import uuid
import json
from random import shuffle

from flask import Flask, jsonify, request
import requests as rq

from utils.client import ClientQueue, should_explode

import pdb

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


# route invoked by client to join the game
@app.route("/join", methods=['POST'])
def join_game():
    ret_val = {
        'message': None
    }

    if close_game['status']:
        ret_val['message'] = \
            'Game is closed. Check with guardian about next round.'

        return jsonify(ret_val)

    data = request.get_json()

    # id corresponds to client IP
    client_id = data['identifier']

    if client_id in valid_clients:
        ret_val['message'] = \
            'Already joined. Please wait for futher instructions.'
        
        return jsonify(ret_val)

    valid_clients.append(client_id)

    ret_val['message'] = 'Successfully joined game. Status: OPEN.'

    return jsonify(ret_val)


# route invoked by guardian to notify that all clients have joined
@app.route("/all_clients", methods=['POST'])
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

    # send notification to first client to begin game
    init_client = cq.peek()

    game_start_msg = {
        "message": "Start Game! Follow the instructions on the interface."
    }

    rq.post("http://%s:8080/io_route" % init_client, 
            data=json.dumps(game_start_msg), headers=json_header)

    return jsonify({'success': True})


# route invoked by client server to send turn
@app.route("/send_turn", methods=['POST'])
def send_turn():
    # return value for client server
    ret_val = {
        'success': True,
        'message': None,
        'retry': False
    }

    # check if valid client is sending a turn
    data = request.get_json()

    client_id = data['identifier']

    if client_id != cq.peek():
        ret_val['success'] = False
        ret_val['message'] = 'It is not your turn. Please await a message to play.'

        return jsonify(ret_val)

    # valid client has sent turn - check that valid card is played
    played_card = data['card']

    if game_state['recently_played'] is None:
        # first player or after burn - valid move
        game_state['recently_played'] = played_card
        
        ret_val['success'] = True
        ret_val['message'] = 'Valid card played. Ending turn.'

        broadcast = {
            'message': '%s played a %s.' % (client_id, played_card)
        }

        for client in valid_clients:
            # broadcast played message to all clients
            if client == client_id:
                continue
            rq.post("http://%s:8080/io_route" % client, 
                    data=json.dumps(broadcast), headers=json_header)

        return jsonify(ret_val)

    prev_card_idx = card_order.index(game_state['recently_played'])
    played_card_idx = card_order.index(played_card)

    if played_card_idx < prev_card_idx:
        # invalid card played, invoke a retry
        ret_val['success'] = False
        ret_val['message'] = 'Invalid card played. Prompting a retry.'
        ret_val['retry'] = True

    # valid card chosen - burn invoked
    if played_card == game_state['recently_played']:
        # broadcast played card
        broadcast = {
            'message': '{client} played a {card} and invoked a Horntail burn.'
        }

        broadcast['message'] = \
            broadcast['message'].format(client=client_id, card=played_card)

        for client in valid_clients:
            # broadcast burn message to all clients
            if client == client_id:
                continue
            
            rq.post("http://%s:8080/io_route" % client, 
                    data=json.dumps(broadcast), headers=json_header)

        # reset game state
        game_state['recently_played'] = None

        # prompt a retry via a message
        ret_val['success'] = True
        ret_val['message'] = \
            'Valid card played, and burn invoked. Please go again.'
    else:
        # broadcast played card
        broadcast = {
            'message': '%s played a %s.' % (client_id, played_card)
        }

        for client in valid_clients:
            # broadcast played message to all clients
            if client == client_id:
                continue

            rq.post("http://%s:8080/io_route" % client,
                    data=json.dumps(broadcast), headers=json_header)

        # end clients turn via dequeue
        cq.dq()

        ret_val['success'] = True
        ret_val['message'] = 'Valid card played. Your turn has ended.'

        # send message to next client
        next_client = cq.peek()

        payload = {
            'message': 'It is your turn.'
        }

        rq.post("http://%s:8080/io_route" % next_client, 
                data=json.dumps(payload), headers=json_header)

    return jsonify(ret_val)



# route invoked by client server to end current client turn - explosion
@app.route("/end_turn", methods=['POST'])
def end_turn():
    # return value for client server
    ret_val = {
        'success': True,
        'message': None
    }

    # check if valid client is ending their turn
    data = request.get_json()

    if data['identifier'] != cq.peek():
        ret_val['success'] = False
        ret_val['message'] = \
            'It is not your turn. Please await a message to play.'

        return jsonify(ret_val)

    # push client to end of queue
    cq.dq()

    ret_val['success'] = True
    ret_val['message'] = 'Turn ended.'

    # make I/O request to next client
    client_id = cq.peek()

    payload = {
        'message': 'It is your turn.'
    }

    rq.post("http://%s:8080/io_route" % client_id, data=json.dumps(payload),
            headers=json_header)

    return jsonify(ret_val)

if __name__ == '__main__':
    # instantiate app server
    app.run(host="0.0.0.0", port=8080, debug=True)
