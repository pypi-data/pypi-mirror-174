import json
from typing import Dict, List, Type

from ..constructors import has_list
from ..trello_requests import get_request, was_successful

from ..base_class import BaseClass


class Board(BaseClass):
    """Board class definition. It holds and interacts with the Lists."""

    def __init__(self, trello: Type[BaseClass], board_id: str) -> None:
        super().__init__(trello.apikey, trello.token)
        self.id = board_id
        self.__lists = []
        self.update()

    @property
    def lists(self) -> List[str]:
        return self.__lists

    def update(self) -> None:
        board = fetch_data(self)
        self.name = board["name"]
        self.closed = board["closed"]
        self.__lists = fetch_lists(self)

    def __str__(self) -> str:
        board = {
            "id": self.id,
            "name": self.name,
            "closed": self.closed,
            "lists": self.lists,
        }
        return json.dumps(board)


def fetch_data(board) -> Dict[str, str]:
    """Loads Board information."""
    url = f"https://api.trello.com/1/boards/{board.id}"
    response = get_request(board, url)
    if was_successful(response):
        board = {
            "name": response["data"]["name"],
            "closed": response["data"]["closed"],
        }
    else:
        board = {"name": None, "closed": None}
    return board


def add_list(board, list_to_add: Dict[str, str]) -> List[str]:
    """Add a new List to the Board."""
    should_add = True
    if len(board.lists) != 0 and has_list(board, list_to_add["id"]):
        for stored_list in board.lists:
            if stored_list["id"] == list_to_add["id"]:
                should_add = False
    if should_add:
        board.lists.append(
            {
                "id": list_to_add["id"],
                "name": list_to_add["name"],
                "closed": list_to_add["closed"],
            }
        )
    return board.lists


def fetch_lists(board) -> Dict[str, str]:
    """Requests all Lists the current Board has from Trello API."""
    url = f"https://api.trello.com/1/boards/{board.id}/lists"
    response = get_request(board, url)
    lists = []
    if was_successful(response):
        for trello_list in response["data"]:
            lists = add_list(board, trello_list)
    return lists
