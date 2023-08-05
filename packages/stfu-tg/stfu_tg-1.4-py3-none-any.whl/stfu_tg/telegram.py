from .formatting import Url


class UserLink(Url):
    user_id: int

    def __init__(self, user_id: int, name: str, link: str):
        super().__init__(name, f'tg://user?id={user_id}')
