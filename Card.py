from enum import Enum


class Suits(Enum):
        DIAMONDS = unichr(0x2666)
        HEARTS = unichr(0x2665)
        CLUBS = unichr(0x2663)
        SPADES = unichr(0x2660)


class Card(object):
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
        self.val = self.get_val_from_number()

    def get_val_from_number(self):
        face_cards = {
            'J': 11,
            'Q': 12,
            'K': 13,
            'A': 14
        }

        if self.number == '2':
            return int(self.number) + 13
        elif self.number <= '9' or self.number == '10':
            return int(self.number)
        elif self.number in face_cards:
            return face_cards[self.number]
        else:
            return ''

    @staticmethod
    def print_ascii_front(card):
        # Generate top, blank middle and bottom rows
        top = unichr(0x250C)
        bottom = unichr(0x2514)
        empty_mid = left = suit_left = middle = right = suit_right = unichr(0x2502)
        for i in range(0, 15):
            top += unichr(0x2500)
            bottom += unichr(0x2500)
            empty_mid += u' '
        top += unichr(0x2510)
        bottom += unichr(0x2518)
        empty_mid += unichr(0x2502)

        # Generate card=specific lines
        left += u'{}'.format(card.number)
        suit_left += u'{}'.format(card.suit)
        for i in range(0, 7):
            middle += u' '
        middle += u'{}'.format(card.suit)
        for i in range(0, 7):
            middle += u' '

        if card.number == '10':
            for i in range(0, 13):
                left += u' '
                right += u' '
        else:
            for i in range(0, 14):
                left += u' '
                right += u' '

        for i in range(0, 14):
            suit_left += u' '
            suit_right += u' '

        right += u'{}'.format(card.number)
        suit_right += u'{}'.format(card.suit)
        left += unichr(0x2502)
        right += unichr(0x2502)
        suit_left += unichr(0x2502)
        suit_right += unichr(0x2502)
        middle += unichr(0x2502)

        lines = [top, left, suit_left, middle, suit_right, right, bottom]
        for i in range(0, 3):
            lines.insert(3, empty_mid)
            lines.insert(len(lines) - 3, empty_mid)
        for l in lines:
            print l


card = Card(Suits.HEARTS, '10')
card2 = Card(Suits.CLUBS, '2')
card3 = Card(Suits.DIAMONDS, 'A')
card4 = Card(Suits.SPADES, 'K')

Card.print_ascii_front(card)
Card.print_ascii_front(card2)
Card.print_ascii_front(card3)
Card.print_ascii_front(card4)
