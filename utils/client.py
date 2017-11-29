"""
    Helper functions and data-structures for client-related mechanics.
"""
import random

explosion_threshold = 95


class ClientQueue:
    def __init__(self):
        self.q = []

    def enq(self, node):
        self.q.append(node)
        return True

    def dq(self, quit=False):
        node = self.q.pop(0)

        if quit:
            return

        # client continues playing
        self.enq(node)

        return

    def peek(self):
        return self.q[0]


def should_explode(num_cards=None):
    # determine whether card in hand should explode
    # randomly generate number between 1 and 100
    # if number > threshold => card explodes

    ri = random.randint(1, 100)

    if num_cards is None:
        return ri >= explosion_threshold
    elif num_cards == 0:
        # can't explode with no cards in hand
        return False, None

    # randomly determine which card should explode
    explode_idx = random.randint(0, num_cards-1)
    return (ri >= explosion_threshold, explode_idx)


def io_print(data, ignore=[], card=False):
    for key, val in data.iteritems():
        if key in ignore:
            continue

        print "\n"

        if not card:
            print "%s : %s" % (key.upper(), val)
        else:
            print val
        
        print "\n"


if __name__ == '__main__':
    cq = ClientQueue()
