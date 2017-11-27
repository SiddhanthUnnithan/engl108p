"""
    Helper functions and data-structures for client-related mechanics.
"""

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


if __name__ == '__main__':
    cq = ClientQueue()
