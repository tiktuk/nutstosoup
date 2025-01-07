"""Module for interacting with the NTS Radio API."""

import requests
from typing import Dict, Any
from requests.exceptions import RequestException, Timeout


class NTSAPIError(Exception):
    """Base exception for NTS API errors."""
    pass


class NTSAPIResponseError(NTSAPIError):
    """Raised when the API returns an unsuccessful status code."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"API returned {status_code}: {message}")


class NTSAPITimeoutError(NTSAPIError):
    """Raised when the API request times out."""
    pass


def fetch_nts_api(endpoint: str, timeout: int = 10) -> Dict[str, Any]:
    """Fetch data from NTS API endpoint.

    Args:
        endpoint: The API endpoint to fetch from (e.g. 'live', 'mixtapes')
        timeout: Request timeout in seconds

    Returns:
        The JSON response as a dict

    Raises:
        NTSAPIResponseError: If the API returns an unsuccessful status code
        NTSAPITimeoutError: If the request times out
        NTSAPIError: For other API-related errors
    """
    try:
        response = requests.get(
            f"https://www.nts.live/api/v2/{endpoint}",
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except Timeout:
        raise NTSAPITimeoutError("Request timed out")
    except RequestException as e:
        if hasattr(e, "response") and e.response is not None:
            raise NTSAPIResponseError(e.response.status_code, str(e))
        raise NTSAPIError(f"Request failed: {str(e)}")


def get_nts_live_data(timeout: int = 10) -> Dict[str, Any]:
    """Fetch current NTS broadcast data.

    Args:
        timeout: Request timeout in seconds

    Returns:
        The live broadcast data as a dict

    Raises:
        NTSAPIResponseError: If the API returns an unsuccessful status code
        NTSAPITimeoutError: If the request times out
        NTSAPIError: For other API-related errors
    """
    return fetch_nts_api("live", timeout)


def get_nts_mixtapes_data(timeout: int = 10) -> Dict[str, Any]:
    """Fetch NTS mixtapes data.

    Args:
        timeout: Request timeout in seconds

    Returns:
        The mixtapes data as a dict

    Raises:
        NTSAPIResponseError: If the API returns an unsuccessful status code
        NTSAPITimeoutError: If the request times out
        NTSAPIError: For other API-related errors
    """
    return fetch_nts_api("mixtapes", timeout)
