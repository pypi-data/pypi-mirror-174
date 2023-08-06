import json
from typing import Dict, List

from .base_class import BaseClass
from .constructors import has_board
from .trello_requests import get_request, was_successful


class User(BaseClass):
    """User class definition. It holds and interacts with the Boards."""

    def __init__(self, apikey: str, token: str) -> None:
        super().__init__(apikey, token)
        self.__boards = []
        self.__boards = fetch_boards(self)
        user = fetch_data(self)
        self.id = user["id"]
        self.__full_name = user["full_name"]
        self.__username = user["username"]

    @property
    def full_name(self) -> str:
        return self.__full_name

    @property
    def username(self) -> str:
        return self.__username

    @property
    def boards(self) -> List[str]:
        return self.__boards

    def __str__(self) -> str:
        user = {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "boards": self.boards,
        }
        return json.dumps(user)


def fetch_data(user) -> Dict[str, str]:
    """Load all User data."""
    url = "https://api.trello.com/1/members/me"
    response = get_request(user, url)
    if was_successful(response):
        user = {
            "id": response["data"]["id"],
            "full_name": response["data"]["fullName"],
            "username": response["data"]["username"],
        }
    else:
        user = {"id": None, "full_name": None, "username": None}
    return user


def fetch_boards(user) -> Dict[str, str]:
    """Requests all Board the current User has from Trello API."""
    url = "https://api.trello.com/1/members/me/boards"
    response = get_request(user, url)
    boards = []
    if was_successful(response):
        for board in response["data"]:
            boards = add_board(user, board)
    return boards


def add_board(user, board: Dict[str, str]) -> List[str]:
    """Add a new Board to the list."""
    should_add = True
    if len(user.boards) != 0 and has_board(user, board["id"]):
        for stored_board in user.boards:
            if stored_board["id"] == board["id"]:
                should_add = False
    if should_add:
        user.boards.append(
            {
                "id": board["id"],
                "name": board["name"],
                "closed": board["closed"],
            }
        )
    return user.boards
