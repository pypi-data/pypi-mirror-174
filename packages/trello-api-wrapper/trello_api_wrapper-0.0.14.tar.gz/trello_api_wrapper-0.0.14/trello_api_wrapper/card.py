from typing import Dict, Type

from .base_class import BaseClass
from .trello_requests import get_request, was_successful


class Card(BaseClass):
    """Card class definition. Those are the main components of the project."""

    def __init__(self, trello: Type[BaseClass], card_id: str) -> None:
        super().__init__(trello.apikey, trello.token)
        self.id = card_id
        self.update()

    def update(self) -> None:
        card = fetch_data(self)
        self.name = card["name"]
        self.closed = card["closed"]


def fetch_data(card) -> Dict[str, str]:
    """Loads CardList information."""
    url = f"https://api.trello.com/1/cards/{card.id}"
    response = get_request(card, url)
    if was_successful(response):
        temp_card = {
            "name": response["data"]["name"],
            "closed": response["data"]["closed"],
        }
    else:
        temp_card = {"name": None, "closed": None}
    return temp_card
