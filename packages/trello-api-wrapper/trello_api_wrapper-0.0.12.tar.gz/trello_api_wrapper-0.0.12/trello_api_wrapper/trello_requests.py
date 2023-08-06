"""Useful request shortcuts."""
from typing import Dict, Type

import httpx

from .base_class import BaseClass


def get_request(
    trello: Type[BaseClass],
    url: str,
    data: Dict[str, str] = None,
) -> Dict[str, str]:
    """Get request with a scent of Trello."""
    data = data or {}
    try:
        headers = {"Accept": "application/json"}
        param = {"key": trello.apikey, "token": trello.token}
        response = httpx.get(url, headers=headers, params={**param, **data})
        response.raise_for_status()
        return {
            "status": response.status_code,
            "url": url,
            "data": response.json(),
        }
    except httpx.HTTPStatusError as exc:
        return {"status": exc.response.status_code, "url": url, "data": []}


def was_successful(response: httpx.Response) -> bool:
    """Check if the response was successful."""
    return len(response) != 0 and response["status"] == 200
