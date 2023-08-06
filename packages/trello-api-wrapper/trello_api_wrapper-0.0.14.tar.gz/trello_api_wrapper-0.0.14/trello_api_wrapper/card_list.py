import json
from typing import Dict, List, Type

import requests

from .base_class import BaseClass
from .constructors import has_card
from .trello_requests import get_request, was_successful

CREATE_CARD_URL = "https://api.trello.com/1/cards"


class CardList(BaseClass):
    """List class definition. It holds and interacts with the Cards."""

    def __init__(self, trello: Type[BaseClass], list_id: str) -> None:
        super().__init__(trello.apikey, trello.token)
        self.id = list_id
        temp_list = fetch_data(self)
        self.name = temp_list["name"]
        self.closed = temp_list["closed"]
        self.__cards = []
        self.__cards = fetch_cards(self)

    @property
    def cards(self) -> List[str]:
        return self.__cards

    def create_card(self, title, description, label_ids):
        """Create a new Trello card"""
        params = {
            "name": title,
            "desc": description,
            "pos": "top",
            "idList": self.id,
            "key": super().apikey,
            "token": super().token,
            "idLabels": label_ids,
        }
        response = requests.request("POST", CREATE_CARD_URL, params=params)
        card_id = response.json()["id"] if response.ok else None
        return card_id, response.status_code

    def __str__(self) -> str:
        card_list = {
            "id": self.id,
            "name": self.name,
            "closed": self.closed,
            "cards": self.cards,
        }
        return json.dumps(card_list)


def fetch_data(card_list) -> Dict[str, str]:
    """Loads CardList information."""
    url = f"https://api.trello.com/1/lists/{card_list.id}"
    response = get_request(card_list, url)
    if was_successful(response):
        temp_list = {
            "name": response["data"]["name"],
            "closed": response["data"]["closed"],
        }
    else:
        temp_list = {"name": None, "closed": None}
    return temp_list


def add_card(card_list, card: Dict[str, str]) -> List[str]:
    """Add a new Card to the List."""
    should_add = True
    if len(card_list.cards) != 0 and has_card(card_list, card["id"]):
        for stored_card in card_list.cards:
            if stored_card["id"] == card["id"]:
                should_add = False
    if should_add:
        card_list.cards.append(
            {
                "id": card["id"],
                "name": card["name"],
                "closed": card["closed"],
            }
        )
    return card_list.cards


def fetch_cards(card_list) -> Dict[str, str]:
    """Requests all Cards the current CardList has from Trello API."""
    url = f"https://api.trello.com/1/lists/{card_list.id}/cards"
    response = get_request(card_list, url)
    cards = []
    if was_successful(response):
        for card in response["data"]:
            cards = add_card(card_list, card)
    return cards
