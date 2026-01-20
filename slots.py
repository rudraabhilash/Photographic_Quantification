import sys

class Normal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Slotted:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

n = Normal(1, 2)
s = Slotted(1, 2)

print("Normal object:", sys.getsizeof(n))
print("Normal __dict__:", sys.getsizeof(n.__dict__))
print("Total normal:", sys.getsizeof(n) + sys.getsizeof(n.__dict__))

print("Slotted object:", sys.getsizeof(s))













"""
python slots.py
Normal object: 48
Normal __dict__: 296
Total normal: 344
Slotted object: 48
"""