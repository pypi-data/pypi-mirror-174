from .base import Core
from .formatting import Bold


class KeyValue(Core):
    def __init__(self, title, value, suffix=': ', title_bold=True):
        self.title = Bold(title) if title_bold else title
        self.value = value
        self.suffix = suffix

    def __str__(self) -> str:
        return f'{self.title}{self.suffix}{self.value}'

    def __repr__(self):
        return str(self)


class HList(Core):
    def __init__(self, *args, prefix='', divider=' '):
        self.items = list(args)
        self.prefix = prefix
        self.divider = divider

    def __iter__(self):
        # Skip None values
        return (x for x in self.items if x)

    def __str__(self) -> str:
        text = ''
        for idx, item in enumerate(self):
            if idx > 0:
                text += self.divider
            if self.prefix:
                text += self.prefix
            text += str(item)

        return text
