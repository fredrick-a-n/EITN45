class Node(object):
    def __init__(self, zero=None, one=None):
        self.zero = zero
        self.one = one
        self.key = ("k")

    def children(self):
        return (self.zero, self.one)

    def __str__(self):
        return '%s_%s' % (self.zero, self.one)