"""
    Client interface used to execute game commands.
"""
import json

import requests as rq

client_url = "http://localhost:8080/%s"

json_headers = {'Content-Type': 'application/json'}

intro2 = """                                         _ __
        ___                             | '  \\
   ___  \ /  ___         ,'\_           | .-. \        /|
   \ /  | |,'__ \  ,'\_  |   \          | | | |      ,' |_   /|
 _ | |  | |\/  \ \ |   \ | |\_|    _    | |_| |   _ '-. .-',' |_   _
// | |  | |____| | | |\_|| |__    //    |     | ,'_`. | | '-. .-',' `. ,'\_
\\\\_| |_,' .-, _  | | |   | |\ \  //    .| |\_/ | / \ || |   | | / |\  \|   \\
 `-. .-'| |/ / | | | |   | | \ \//     |  |    | | | || |   | | | |_\ || |\_|
   | |  | || \_| | | |   /_\  \ /      | |`    | | | || |   | | | .---'| |
   | |  | |\___,_\ /_\ _      //       | |     | \_/ || |   | | | |  /\| |
   /_\  | |           //_____//       .||`      `._,' | |   | | \ `-' /| |
        /_\           `------'        \ |   AND        `.\  | |  `._,' /_\\
                                       \|       THE          `.\\
                                            ___      __        __   __          __
                                           |__  \_/ |__) |    /  \ |  \ | |\ | / _`
                                           |___ / \ |    |___ \__/ |__/ | | \| \__>
                                                 __   __   ___  __     __   ___      ___
                                                |__) |__) |__  /__` | |  \ |__  |\ |  |
                                                |    |  \ |___ .__/ | |__/ |___ | \|  |
                                                                                         """

welcome_msg = \
"""
Welcome to Explosive Harry Potter themed President!
The game is very similar to the original President card game, with the inclusion of randomly exploding cards.

Game Mechanics
--------------
1. Every card played must be higher (number-wise) than the previous.
2. If the card played is numerically identical to the previous card played, the player invokes a Horntail burn! The player is prompted to go again.
3. The game currently only supports single card plays. Future iterations will include double and triple plays.
4. The card order is as follows: [lowest - highest] 3 - 10, J, Q, K, A, 2
5. Cards may explode at two points:
    1) Requesting to see one's hand.
    2) Playing a card.
\n
"""

command_msg = \
"""
Game Interface Commands
-----------------------
G: Get your hand. The presented cards are tagged with numbers that you will use when playing a card. You can request to see your hand at any point.

E: End your turn. You can only execute this command if it is your turn. This is equivalent to 'passing' in the original game.

P: Play your card. This command requires additional specification of which card should be played. You are required to specify the index of the card as it is presented to you when you ask to 'view' your hand.

L: View the last played card. Remember that suit is not important in this game.

Q: Quit the game. You can only quit the game if all of your cards are done.
\n
"""


def game_loop():
    # simple commands
    simple_commands = {
        'G': lambda _: rq.get(client_url % "get_hand"),
        'E': lambda _: rq.get(client_url % "end_turn"),
        'I': None,
        'Q': lambda _: rq.get(client_url % "end_game"),
        'P': None,
        'L': lambda _: rq.get(client_url % "last_played")
    }

    print intro2

    print welcome_msg

    print command_msg

    while True:
        print "Input 'I' if you would like to see the game interface commands.\n"

        user_input = raw_input("Interface input:")
        user_input = user_input.strip().upper()

        if user_input not in simple_commands:
            print "Incorrect input specified. Please try again.\n"
            continue
        elif user_input == 'I':
            print command_msg
        elif user_input == 'P': # check if card is being played
            print "Please specify which card you would like to play.\n"

            # get hand output logged to console
            res = simple_commands['G'](None)

            # get last played card
            res = simple_commands['L'](None)

            card_index = raw_input("Card index:")

            try:
                card_index = int(card_index)
            except:
                print "The passed index must be numerical.\n"
                continue

            data = {
                'card_index': card_index
            }

            res = rq.post(client_url % "send_turn", data=json.dumps(data),
                          headers=json_headers)

            res = json.loads(res.text)

            if not res['success']:
                # propagated error message
                print res['message']
                continue

            print res['message']
        else:
            res = simple_commands[user_input](None)

            if 'success' in res:
                if not res['success']:
                    print res['message']
                    continue

            if 'message' in res:
                print res['message']

    return

if __name__ == '__main__':
    game_loop()
