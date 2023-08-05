from typing import Any


class Core:
    pass


class Doc(Core):
    def __init__(self, *args):
        self.items = list(args)

    def __iter__(self):
        # Skip None values
        return (x for x in self.items if x)

    def __str__(self) -> str:
        return '\n'.join([str(items) for items in self])

    def add(self, other: Any):
        self.items.append(other)
        return self

    def __add__(self, other):
        return self.add(other)

    def __repr__(self):
        return str(self)
