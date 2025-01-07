"""Module for interacting with the NTS Radio API."""

import requests
from dataclasses import dataclass
from typing import Dict, Any, List
from requests.exceptions import RequestException, Timeout


@dataclass
class Broadcast:
    """Represents a live broadcast on an NTS channel."""

    channel: str
    title: str
    start_time: str
    end_time: str
    name: str | None = None
    description: str | None = None
    location_short: str | None = None
    location_long: str | None = None
    show_alias: str | None = None
    episode_alias: str | None = None
    picture_url: str | None = None
    raw_json: Dict[str, Any] | None = None


@dataclass
class Mixtape:
    """Represents an NTS mixtape."""

    title: str
    subtitle: str
    description: str
    stream_url: str
    mixtape_alias: str
    picture_url: str | None = None
    credits: list[dict[str, str]] | None = None
    raw_json: Dict[str, Any] | None = None


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
            f"https://www.nts.live/api/v2/{endpoint}", timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except Timeout:
        raise NTSAPITimeoutError("Request timed out")
    except RequestException as e:
        if "404" in str(e):
            raise NTSAPIResponseError(404, str(e))
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


def get_mixtapes(timeout: int = 10) -> Dict[str, Mixtape]:
    """Get a simplified dictionary of NTS mixtapes.

    Args:
        timeout: Request timeout in seconds

    Returns:
        Dictionary with mixtape aliases as keys and mixtape info as values

    Raises:
        NTSAPIResponseError: If the API returns an unsuccessful status code
        NTSAPITimeoutError: If the request times out
        NTSAPIError: For other API-related errors
    """
    mixtapes_data = get_nts_mixtapes_data(timeout)

    if not mixtapes_data or "results" not in mixtapes_data:
        raise NTSAPIError("Invalid mixtapes data format")

    mixtapes = {}
    for mixtape in mixtapes_data["results"]:
        picture_url = mixtape.get("media", {}).get("picture_large")
        mixtapes[mixtape["mixtape_alias"]] = Mixtape(
            title=mixtape["title"],
            subtitle=mixtape["subtitle"],
            description=mixtape["description"],
            stream_url=mixtape["audio_stream_endpoint"],
            mixtape_alias=mixtape["mixtape_alias"],
            picture_url=picture_url,
            credits=mixtape.get("credits"),
            raw_json=mixtape,
        )

    return mixtapes


def get_current_broadcasts(timeout: int = 10) -> List[Broadcast]:
    """Get a list of current broadcasts for both NTS channels.

    Args:
        timeout: Request timeout in seconds

    Returns:
        List of current broadcasts

    Raises:
        NTSAPIResponseError: If the API returns an unsuccessful status code
        NTSAPITimeoutError: If the request times out
        NTSAPIError: For other API-related errors
    """
    live_data = get_nts_live_data(timeout)

    if not live_data or "results" not in live_data:
        raise NTSAPIError("Invalid live data format")

    broadcasts = []
    for channel in live_data["results"]:
        if "now" in channel:
            broadcast = channel["now"]
            details = broadcast.get("embeds", {}).get("details", {})
            picture_url = details.get("media", {}).get("picture_large")
            broadcasts.append(
                Broadcast(
                    channel=channel["channel_name"],
                    title=broadcast["broadcast_title"],
                    start_time=broadcast["start_timestamp"],
                    end_time=broadcast["end_timestamp"],
                    name=details.get("name"),
                    description=details.get("description"),
                    location_short=details.get("location_short"),
                    location_long=details.get("location_long"),
                    show_alias=details.get("show_alias"),
                    episode_alias=details.get("episode_alias"),
                    picture_url=picture_url,
                    raw_json=broadcast,
                )
            )

    return broadcasts
