from typing import Any, List

from .base import Doc, Core
from .formatting import Bold, Underline


class SectionCore(Core):
    items: List[Any]

    def add(self, other: Any):
        self.items.append(other)
        return self

    def __add__(self, other):
        return Doc(self, other)

    def __iadd__(self, other):
        return self.add(other)

    def __iter__(self):
        # Skip None values
        return (x for x in self.items if x)

    def __repr__(self):
        return str(self)


class Section(SectionCore):
    def __init__(
            self,
            *args,
            title: str = '',
            title_underline=True,
            title_bold=True,
            indent=1,
            indent_text='  ',
            postfix=':'
    ):
        self.title_text = title
        self.items = list(args)
        self.indent = indent
        self.title_underline = title_underline
        self.title_bold = title_bold
        self.indent_text = indent_text
        self.postfix = postfix

    @property
    def title(self) -> str:
        if not self.title_text:
            return ''

        title = Underline(self.title_text) if self.title_underline else self.title_text
        title = Bold(title) if self.title_bold else title
        return str(title) + self.postfix

    def to_str(self, additional_indent: int = 0) -> str:
        text = ''
        text += self.title
        for item in self:
            text += '\n'

            if type(item) is Section:
                text += self.indent_text * (self.indent + additional_indent)
                text += item.to_str(additional_indent=additional_indent + self.indent)
            elif type(item) is VList:
                text += item.to_str(additional_indent=(additional_indent + self.indent) * 2)
            else:
                text += self.indent_text * (self.indent + additional_indent)
                text += str(item)

        return text

    def __str__(self) -> str:
        return self.to_str()


class VList(SectionCore):
    def __init__(self, *args, indent=0, prefix='- '):
        self.items = list(args)
        self.prefix = prefix
        self.indent = indent

    def to_str(self, additional_indent: int = 0) -> str:
        indent = self.indent + additional_indent
        space = ' ' * indent if indent else ' '
        text = ''
        for idx, item in enumerate(self):
            if idx > 0:
                text += '\n'
            text += f'{space}{self.prefix}{item}'

        return text

    def __str__(self) -> str:
        return self.to_str()
