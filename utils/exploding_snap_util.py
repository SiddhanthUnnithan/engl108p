from Card import Card, Suits
from random import randint, choice
from datetime import datetime
import os
import random

suit_list = list(Suits)

face_cards = {
            'J': 11,
            'Q': 12,
            'K': 13,
            'A': 14
        }

intro = """                                         _ __
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
                                                                         __             __
                                                                        /__` |\ |  /\  |__)
                                                                        .__/ | \| /~~\ |\n"""

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


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_two_cards(card1, card2):
    for a, b in zip(card1.get_ascii_front(), card2.get_ascii_front()):
        print u'{} {}'.format(a, b)


def get_random_card():
    """
    Generates a purely random card from a standard deck using a unique seed
    :return: Card object
    """
    random.seed(datetime.now())
    suit = choice(suit_list)
    rand = randint(2, 14)
    number = get_number_from_val(rand)
    return Card(suit, number)


def get_second_card(first_card):
    """
    Generates a pseudo-random second card; improves likelihood of two same numbers showing up to 20%
    :param first_card: Randomly generated first card
    :return: Card object
    """
    possible_cards = []
    first_val = first_card.val
    possible_cards.append(first_val)
    for i in range(0, 3):
        rand = randint(2, 14)
        # Ensure only a non-first_val number is inserted, to maintain 20% probability
        while rand != first_val:
            possible_cards.append(rand)
            break

    suit = choice(suit_list)
    number = get_number_from_val(choice(possible_cards))
    return Card(suit, number)


def get_number_from_val(value):
    number = 2
    if value < 11:
        number = str(value)
    else:
        for key, val in face_cards.iteritems():
            if value == val:
                number = key
    return number
