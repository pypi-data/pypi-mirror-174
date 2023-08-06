from .trello_requests import get_request


def has_board(user, board_id: str) -> bool:
    """Check if the Board exists for User."""
    url = f"https://api.trello.com/1/boards/{board_id}"
    response = get_request(user, url)
    return response["status"] == 200


def has_list(board, list_id: str) -> bool:
    """Check if the List exists on the Board."""
    url = f"https://api.trello.com/1/lists/{list_id}"
    response = get_request(board, url)
    return response["status"] == 200


def has_card(card_list, card_id: str) -> bool:
    """Check if the Card exists on the List."""
    url = f"https://api.trello.com/1/cards/{card_id}"
    response = get_request(card_list, url)
    return response["status"] == 200
