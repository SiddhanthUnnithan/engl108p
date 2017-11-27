"""
    Client server.
"""
import json
import commands

from flask import Flask, jsonify, request
import requests as rq

app = Flask(__name__)

# assumption: all clients are going to be instantiated on OSX machines
ip_addr = commands.getstatusoutput("ipconfig getifaddr en0")[1]

# current_hand
hand = {
    'hand': None
}

# route for server output - logged to console
@app.route("/io_route", methods=['POST'])
def io_route():
    data = request.get_json()
    data = json.loads(data)

    for key, val in data.iteritems():
        print "%s:%s" % (key.upper(), val)
        print "\n"

    return True


@app.route("/post_hand", methods=['POST'])
def post_hand():
    data = request.get_json()
    data = json.loads(data)

    if 'hand' not in data:
        return False

    hand['hand'] = data['hand']

    return True


@app.route("/get_hand", methods=['GET'])
def get_hand():
    ret_val = {
        'hand': hand['hand']
    }

    return jsonify(ret_val)
