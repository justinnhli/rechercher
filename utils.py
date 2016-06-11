from collections import namedtuple
from heapq import heappush, heappop

class PriorityQueue:
    Pair = namedtuple("Pair", ("priority", "item"))
    def __init__(self):
        self.queue = []
        self.items = {}
    def __contains__(self, item):
        return item in self.items
    def __bool__(self):
        return len(self.queue) > 0
    def push(self, item, priority):
        assert item is not None and item not in self.items
        pair = PriorityQueue.Pair(priority, item)
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
            del self.items[item]
        else:
            raise KeyError(item)
    def get_priority(self, item):
        if item in self.items:
            return self.items[item].priority
        else:
            raise KeyError(item)
    def set_priority(self, item, priority):
        if item in self.items:
            self.items[item] = priority
        else:
            self.push(item, priority)

class Namespace:
    def __init__(self, **kwargs):
        self.update(**kwargs)
    def __eq__(self, other):
        if not isinstance(other, Namespace):
            return False
        return vars(self) == vars(other)
    def __len__(self):
        return len(self.__dict__)
    def __add__(self, other):
        updated = self.__dict__
        updated.update(other.__dict__)
        return Namespace(**updated)
    def __contains__(self, key):
        return key in self.__dict__
    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)
    def __setitem__(self, key, value):
        setattr(self, key, value)
    def __delitem__(self, key):
        if key in self.__dict__:
            delattr(self, key)
        raise KeyError(key)
    def __str__(self):
        return 'Namespace(' + ', '.join('{}={}'.format(k, v) for k, v in sorted(self.__dict__.items())) + ')'
    def update(self, **kwargs):
        for key, value in kwargs.items():
            self[key] = value
    def keys(self):
        return self.__dict__.keys()
    def values(self):
        return self.__dict__.values()
    def items(self):
        return self.__dict__.items()
