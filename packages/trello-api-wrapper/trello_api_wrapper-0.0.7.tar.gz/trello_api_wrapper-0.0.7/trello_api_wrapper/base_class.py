"""Base Class for all trello based objects."""
import json


class BaseClass:
    def __init__(self, apikey: str, token: str) -> None:
        self.__apikey = apikey
        self.__token = token
        self.__id = None
        self.__name = "undefined"
        self.__closed = False

    @property
    def apikey(self) -> str:
        return self.__apikey

    @property
    def token(self) -> str:
        return self.__token

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, new_id: str) -> None:
        self.__id = new_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name: str) -> None:
        self.__name = new_name

    @property
    def closed(self) -> bool:
        return self.__closed

    @closed.setter
    def closed(self, new_closed: bool) -> None:
        self.__closed = new_closed

    def __str__(self) -> str:
        base_class = {"id": self.id, "name": self.name, "closed": self.closed}
        return json.dumps(base_class)
