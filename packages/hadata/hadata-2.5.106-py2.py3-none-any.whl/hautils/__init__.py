"""
hautils.

An example python library.
"""

__version__ = "0.2.0"
__author__ = 'Nayana Hettiarachchi'
__credits__ = 'HiAcuity Labs'

import os
from collections import deque


class DeQueue(deque):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.que = deque()

    def append(self, item):
        self.que.append(item)

    def clear(self):
        self.que.clear()

    def push(self, item):
        if os.getenv("APP_NAME") != "backend":
            from hautils.deque import add_to_rmq
            add_to_rmq(item)
        else:
            self.append(item)
    def popleft(self):
        return self.que.popleft()

    def pop(self):
        return self.que.pop()

    def peek(self):
        return self.que[0]

    def empty(self):
        return len(self.que) == 0

    def __len__(self):
        return self.que.__len__()

    def __str__(self):
        return self.que.__str__()

    def __repr__(self):
        return self.que.__repr__()


ha_que = DeQueue()

if ha_que is None:
    ha_que = DeQueue()
