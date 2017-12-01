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

    def get_ascii_front(self):
        # Generate top, blank middle and bottom rows
        top = unichr(0x250C)
        bottom = unichr(0x2514)
        empty_mid = left = suit_left = middle = face = twomid = right = suit_right = unichr(0x2502)
        for i in range(0, 19):
            top += unichr(0x2500)
            bottom += unichr(0x2500)
            empty_mid += u' '
        top += unichr(0x2510)
        bottom += unichr(0x2518)
        empty_mid += unichr(0x2502)

        # Generate Single Middle and Face Cards
        for i in range(0, 9):
            middle += u' '
            face += u' '
        middle += u'{}'.format(self.suit)
        face += u'{}'.format(self.number)
        for i in range(0, 9):
            middle += u' '
            face += u' '
        middle += unichr(0x2502)
        face += unichr(0x2502)

        # Generate Double Middle Symbol
        twomid += u'  '
        twomid += u'{}'.format(self.suit)
        for i in range(0, 13):
            twomid += u' '
        twomid += u'{}'.format(self.suit)
        twomid += u'  '
        twomid += unichr(0x2502)

        # Generate card-specific lines
        left += u'{}'.format(self.number)
        suit_left += u'{}'.format(self.suit)

        if self.number == '10':
            for i in range(0, 17):
                left += u' '
                right += u' '
        else:
            for i in range(0, 18):
                left += u' '
                right += u' '

        for i in range(0, 18):
            suit_left += u' '
            suit_right += u' '

        right += u'{}'.format(self.number)
        suit_right += u'{}'.format(self.suit)
        left += unichr(0x2502)
        right += unichr(0x2502)
        suit_left += unichr(0x2502)
        suit_right += unichr(0x2502)

        lines = [top, left, suit_left, suit_right, right, bottom]
        if self.number in ['J', 'Q', 'K', 'A']:
            if self.number == 'A':
                lines.insert(3, middle)
            else:
                lines.insert(3, face)
            for i in range(0, 4):
                lines.insert(3, empty_mid)
                lines.insert(len(lines) - 3, empty_mid)
        elif self.number == '2':
            lines.insert(3, middle)
            for i in range(0, 7):
                lines.insert(3, empty_mid)
            lines.insert(3, middle)
        elif self.number == '3':
            lines.insert(3, empty_mid)
            lines.insert(4, middle)
            for i in range(0, 2):
                lines.insert(5, middle)
                lines.insert(5, empty_mid)
                lines.insert(5, empty_mid)
            lines.insert(len(lines) - 3, empty_mid)
        elif self.number == '4':
            lines.insert(3, twomid)
            for i in range(0, 7):
                lines.insert(4, empty_mid)
            lines.insert(len(lines) - 3, twomid)
        elif self.number == '5':
            lines.insert(3, twomid)
            lines.insert(3, middle)
            lines.insert(3, twomid)
            for i in range(0, 3):
                lines.insert(4, empty_mid)
                lines.insert(len(lines) - 4, empty_mid)
        elif self.number == '6':
            lines.insert(3, twomid)
            for i in range(0, 2):
                lines.insert(3, twomid)
                lines.insert(4, empty_mid)
                lines.insert(4, empty_mid)
                lines.insert(4, empty_mid)
        elif self.number == '7':
            lines.insert(3, twomid)
            lines.insert(4, empty_mid)
            lines.insert(5, middle)
            lines.insert(6, empty_mid)
            lines.insert(7, twomid)
            lines.insert(8, empty_mid)
            lines.insert(8, empty_mid)
            lines.insert(8, empty_mid)
            lines.insert(len(lines) - 3, twomid)
        elif self.number == '8':
            lines.insert(3, twomid)
            lines.insert(4, empty_mid)
            lines.insert(5, middle)
            lines.insert(6, empty_mid)
            lines.insert(7, twomid)
            lines.insert(8, empty_mid)
            lines.insert(9, middle)
            lines.insert(10, empty_mid)
            lines.insert(11, twomid)
        elif self.number == '9':
            lines.insert(3, twomid)
            lines.insert(4, empty_mid)
            lines.insert(5, empty_mid)
            lines.insert(6, twomid)
            lines.insert(7, middle)
            lines.insert(8, twomid)
            lines.insert(9, empty_mid)
            lines.insert(10, empty_mid)
            lines.insert(11, twomid)
        elif self.number == '10':
            lines.insert(3, empty_mid)
            lines.insert(4, twomid)
            lines.insert(5, middle)
            lines.insert(6, twomid)
            lines.insert(7, empty_mid)
            lines.insert(8, twomid)
            lines.insert(9, middle)
            lines.insert(10, twomid)
            lines.insert(11, empty_mid)

        return lines
