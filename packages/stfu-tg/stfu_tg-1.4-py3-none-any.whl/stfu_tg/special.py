from stfu_tg.base import Core


class InvisibleSymbol(Core, str):
    def __str__(self):
        return '&#8288;'
