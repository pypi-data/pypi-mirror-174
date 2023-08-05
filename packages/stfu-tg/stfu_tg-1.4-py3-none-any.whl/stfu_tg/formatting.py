import html
from typing import Any, Optional

from stfu_tg.base import Core


class StyleFormationCore(Core):
    start: str
    end: str

    def __init__(self, data: Any):
        if not isinstance(data, Core):
            data = html.escape(str(data))

        self.text = f'{self.start}{data}{self.end}'

    def __str__(self) -> str:
        return self.text

    def __repr__(self):
        return str(self)


class Bold(StyleFormationCore):
    start = '<b>'
    end = '</b>'


class Italic(StyleFormationCore):
    start = '<i>'
    end = '</i>'


class Code(StyleFormationCore):
    start = '<code>'
    end = '</code>'


class Pre(StyleFormationCore):
    start = '<pre>'
    start_language = '<pre><code class="language-{}">'
    end = '</pre>'
    language: Optional[str]

    def __init__(self, data: Any, language: Optional[str] = None):
        text = html.escape(str(data))

        self.language = language
        if language is None:
            self.text = f'{self.start}{text}{self.end}'
        else:
            self.text = f'{self.start_language.format(self.language)}{text}{self.end}'


class Strikethrough(StyleFormationCore):
    start = '<s>'
    end = '</s>'


class Underline(StyleFormationCore):
    start = '<u>'
    end = '</u>'


class Spoiler(StyleFormationCore):
    start = '<tg-spoiler>'
    end = '</tg-spoiler>'


class Url(StyleFormationCore):
    start = '<a href="{}">'
    end = '</a>'

    def __init__(self, name: Any, link: str):
        self.start = self.start.format(html.escape(link))
        super().__init__(name)
