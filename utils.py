from collections import namedtuple
from heapq import heappush, heappop

class PriorityQueue:
    Pair = namedtuple("Pair", ("priority", "item"))
    def __init__(self, key_fn):
        self.queue = []
        self.key_fn = key_fn
        self.items = {}
        self.removed = set()
    def __contains__(self, item):
        return item in self.items
    def push(self, item):
        assert item is not None and item not in self.items
        pair = PriorityQueue.Pair(self.key_fn(item), item)
        self.items[item] = pair
        heappush(self.queue, pair)
    def pop(self):
        while self.queue:
            pair = heappop(self.queue)
            if pair.item is not None:
                del self.items[pair.item]
                return pair.item
    def remove(self, item):
        if item in self.items:
            self.items[item].item = None
        else:
            raise KeyError(item)
    def get_priority(self, item):
        if item in self.items:
            return self.items[item].priority
        else:
            raise KeyError(item)
