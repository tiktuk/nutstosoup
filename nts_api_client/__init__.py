"""NTS API client module for interacting with the NTS Radio API."""

import requests
from typing import Tuple, Dict, Optional, Any


def fetch_nts_api(endpoint: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Fetch data from NTS API endpoint.

    Args:
        endpoint: The API endpoint to fetch from (e.g. 'live', 'mixtapes')

    Returns:
        Tuple containing:
        - The JSON response as a dict if successful, None if failed
        - An error message string if failed, None if successful
    """
    try:
        response = requests.get(f"https://www.nts.live/api/v2/{endpoint}")
        return response.json(), None
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.RequestException,
    ):
        return None, "Network error: Could not connect to the NTS API"


def get_nts_live_data() -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Fetch current NTS broadcast data.

    Returns:
        Tuple containing:
        - The live broadcast data as a dict if successful, None if failed
        - An error message string if failed, None if successful
    """
    return fetch_nts_api("live")


def get_nts_mixtapes_data() -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Fetch NTS mixtapes data.

    Returns:
        Tuple containing:
        - The mixtapes data as a dict if successful, None if failed
        - An error message string if failed, None if successful
    """
    return fetch_nts_api("mixtapes")
