"""
    Client server.
"""
import json
import commands
import sys
import random

from flask import Flask, jsonify, request
import requests as rq

app = Flask(__name__)

# assumption: all clients are going to be instantiated on OSX machines
ip_addr = commands.getstatusoutput("ipconfig getifaddr en0")[1]

# current_hand
hand = {
    'hand': None
}

# misc variables
explosion_threshold = 95

# route for server output - logged to console
@app.route("/io_route", methods=['POST'])
def io_route():
    data = request.get_json()
    data = json.loads(data)

    for key, val in data.iteritems():
        print "%s:%s" % (key.upper(), val)
        print "\n"

    return True


# route invoked by game server to send client hand
@app.route("/post_hand", methods=['POST'])
def post_hand():
    data = request.get_json()
    data = json.loads(data)

    if 'hand' not in data:
        return False

    hand['hand'] = data['hand']

    return True


# route invoked by client interface to get hand
@app.route("/get_hand", methods=['GET'])
def get_hand():
    ret_val = {
        'hand': hand['hand']
    }

    if hand is not None:
        # determine whether card in hand should explode
        # randomly generate number between 1 and 100
        # if number > threshold => card explodes
        # this threshold can 

        ri = random.randint(1, 100)

        if ri < explosion_threshold:
            # don't explode
            return jsonify(ret_val)

        # randomly determine which card should explode
        explode_idx = random.randint(0, len(hand['hand']))
        hand['hand'].pop(explode_idx)
        ret_val['hand'] = hand['hand']
    
    return jsonify(ret_val)


if __name__ == '__main__':
    # send request to game server to join
    data = {
        'identifer': ip_addr
    }

    headers = {
        'Content-Type': 'application/json'
    }

    res = rq.post("http://%s:8080/join" % sys.env['GAME_SERVER_IP'], 
                  data=json.dumps(data), headers=headers)

    print res['message'] + "\n"

    # instantiate app server
    app.run(host="0.0.0.0", port=8080, debug=True)
