"""
    Convenience script to execute send-turn command.
"""
import sys
import json

import requests as rq

def main(card_idx):
    url = "http://localhost:8080/send_turn"

    data = {
        'card_index': int(card_idx)
    }

    headers = {
        'Content-Type': 'application/json'
    }

    res = rq.post(url, data=json.dumps(data), headers=headers)

    print json.loads(res.text)


if __name__ == '__main__':
    card_idx = sys.argv[1]

    main(card_idx)
