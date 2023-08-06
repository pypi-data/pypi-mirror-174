from typing import Type

from .board import Board
from .card import Card
from .card_list import CardList
from .constructors import has_board, has_card, has_list
from .user import User


class Trello(User):
    def user(self) -> Type[User]:
        """Instantiate a new Trello User."""
        return User(self.apikey, self.token)

    def board(self, board_id: str) -> Type[Board]:
        """Get by ID a new instance of a Board the User has."""
        return Board(self, board_id) if has_board(self, board_id) else None

    def card_list(self, list_id: str) -> Type[CardList]:
        """Get by ID a new instance of a CardList the Board has."""
        return CardList(self, list_id) if has_list(self, list_id) else None

    def card(self, card_id: str) -> Type[Card]:
        """Get by ID a new instance of a Card the CardList has."""
        return Card(self, card_id) if has_card(self, card_id) else None
