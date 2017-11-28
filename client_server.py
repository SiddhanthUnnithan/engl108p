"""
    Client server.
"""
import json
import commands
import os
import random
import logging

from flask import Flask, jsonify, request
import requests as rq

from utils.client import should_explode

import pdb

app = Flask(__name__)

# logging config
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# assumption: all clients are going to be instantiated on OSX machines
if 'DEV_FLAG' in os.environ:
    client_identifier = os.environ['CLIENT_HOSTNAME']
    game_server = "http://%s:8080/" % os.environ['GAME_SERVER_HOSTNAME']
else:
    client_identifier = commands.getstatusoutput("ipconfig getifaddr en0")[1]
    game_server = "http://%s:8080/" % os.environ['GAME_SERVER_IP']

# current_hand
hand = {
    'hand': None
}

# misc variables
explosion_threshold = 95
json_headers = {
    'Content-Type': 'application/json'
}


# route for server output - logged to console
@app.route("/io_route", methods=['POST'])
def io_route():
    data = request.get_json()

    for key, val in data.iteritems():
        print "\n"
        print "%s : %s" % (key.upper(), val)
        print "\n"

    return jsonify({'success': True})


# route invoked by game server to send client hand
@app.route("/post_hand", methods=['POST'])
def post_hand():
    data = request.get_json()
    hand['hand'] = data['hand']
    return jsonify({'success': True})


# route invoked by client interface to get hand
@app.route("/get_hand", methods=['GET'])
def get_hand():
    ret_val = {
        'hand': hand['hand'],
        'message': None
    }

    if hand is not None:
        explode_flag, card_idx = should_explode(len(hand['hand']))

        if not explode_flag:
            # don't explode
            return jsonify(ret_val)

        # randomly determine which card should explode
        exploded_card = hand['hand'].pop(card_idx)

        ret_val['message'] = \
            'Oh no - %s exploded from your hand!' % exploded_card

        ret_val['hand'] = hand['hand']
    
    return jsonify(ret_val)


# route invoked by client interface to send turn to game server
@app.route("/send_turn", methods=['POST'])
def send_turn():
    # return value for interface
    ret_val = {
        'success': True,
        'message': None,
        'retry': False
    }

    # payload for game server
    payload = {
        'identifier': client_identifier,
        'card': None
    }

    data = request.get_json()

    # received data is index of card to be played, or pass message
    card_idx = data['card_index']

    if isisntance(card_idx, str) and card_idx == 'pass':
        # invoke end of turn
        res = rq.post(game_server + "end_turn", data=json.dumps(payload), 
                      headers=json_headers)

        res = json.loads(res.text)

        ret_val['success'] = res['success']
        ret_val['message'] = res['message']

        return ret_val


    if card_idx < 0 or card_idx >= len(hand['hand']):
        ret_val['success'] = False
        ret_val['message'] = 'Invalid card specified. Please try again'

        return ret_val

    # chance that card explodes when it is attempted to play
    explode_flag = should_explode()

    if explode_flag:
        # card explodes - end turn
        exploded_card = hand['hand'].pop(card_idx)
        ret_val['success'] = True
        ret_val['message'] = \
            'Oh no - %s exploded from your hand! Your turn is done.' \
                % exploded_card

        # invoke end of turn
        res = rq.post(game_server + "end_turn", data=json.dumps(payload), 
                headers=json_headers)

        res = json.loads(res.text)

        if not res['success']: # incorrect client id
            res.insert(card_idx, exploded_card)
            ret_val['success'] = res['success']
            ret_val['message'] = res['message']

        return ret_val

    card = hand['hand'][card_idx]

    # hold onto card in case of invalid move
    payload['card'] = card

    res = rq.post(game_server + "send_turn", data=json.dumps(payload),
                  headers=json_headers)

    res = json.loads(res.text)

    # unsuccessful - incorrect move execution
    if not res['success']:
        ret_val['success'] = res['success']
        ret_val['message'] = res['message']
        ret_val['retry'] = res['retry']

        return ret_val

    # successful - turn ending handled on game server side
    # possible that a retry is initiated - done on game server
    # we remove the card from this client's hand
    hand['hand'].pop(card_idx)

    ret_val['success'] = True
    ret_val['message'] = res['message']

    return ret_val


# route invoked by interface to end turn
@app.route("/end_turn")
def end_turn():
    payload = {
        'identifier': client_identifier
    }

    res = rq.post(game_server + "end_turn", data=json.dumps(payload), 
                  headers=json_headers)

    res = json.loads(res.text)

    return jsonify(res)


if __name__ == '__main__':
    # send request to game server to join
    data = {
        'identifier': client_identifier
    }

    res = rq.post(game_server + "join", data=json.dumps(data), 
                  headers=json_headers)

    res = json.loads(res.text)

    print res['message'] + "\n"

    # instantiate app server
    app.run(host="0.0.0.0", port=8080, debug=True)
