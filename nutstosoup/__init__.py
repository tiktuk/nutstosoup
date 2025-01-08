"""Module for interacting with the NTS Radio API."""

import html
import requests
from typing import Dict, Any, List
from requests.exceptions import RequestException, Timeout

from .models import (
    AudioSource,
    BroadcastMedia,
    Broadcast,
    Details,
    Embeds,
    Genre,
    Link,
    Mixtape,
    MixtapeCredit,
    MixtapeMedia,
    Mood,
)

__all__ = [
    # Public API functions
    "fetch_nts_api",
    "get_nts_live_data",
    "get_nts_mixtapes_data",
    "get_mixtapes",
    "get_current_broadcasts",
    # Exceptions
    "NTSAPIError",
    "NTSAPIResponseError",
    "NTSAPITimeoutError",
    # Data models
    "AudioSource",
    "BroadcastMedia",
    "Broadcast",
    "Details", 
    "Embeds",
    "Genre",
    "Link",
    "Mixtape",
    "MixtapeCredit",
    "MixtapeMedia",
    "Mood",
]


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
    """Get a dictionary of NTS mixtapes.

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
        # Create media
        media = MixtapeMedia(**mixtape.get("media", {}))

        # Create credits
        credits = [MixtapeCredit(**credit) for credit in mixtape.get("credits", [])]

        # Create links
        links = [Link(**link) for link in mixtape.get("links", [])]

        # Create mixtape
        mixtapes[mixtape["mixtape_alias"]] = Mixtape(
            mixtape_alias=mixtape["mixtape_alias"],
            title=mixtape["title"],
            subtitle=mixtape["subtitle"],
            description=mixtape["description"],
            description_html=mixtape["description_html"],
            audio_stream_endpoint=mixtape["audio_stream_endpoint"],
            credits=credits,
            media=media,
            now_playing_topic=mixtape.get("now_playing_topic", ""),
            links=links,
            raw_json=mixtape
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
            broadcast_data = channel["now"]
            details_data = broadcast_data.get("embeds", {}).get("details", {})

            # Create Media object
            media = (
                BroadcastMedia(**details_data.get("media", {}))
                if details_data.get("media")
                else BroadcastMedia()
            )

            # Create Links
            links = [Link(**link) for link in broadcast_data.get("links", [])]

            # Create Genres and Moods
            genres = [Genre(**genre) for genre in details_data.get("genres", [])]
            moods = [Mood(**mood) for mood in details_data.get("moods", [])]

            # Create AudioSources
            audio_sources = [
                AudioSource(**source)
                for source in details_data.get("audio_sources", [])
            ]

            # Create Details
            details = Details(
                status=details_data.get("status", ""),
                updated=details_data.get("updated", ""),
                name=details_data.get("name", ""),
                description=details_data.get("description", ""),
                description_html=details_data.get("description_html", ""),
                external_links=details_data.get("external_links", []),
                moods=moods,
                genres=genres,
                location_short=details_data.get("location_short"),
                location_long=details_data.get("location_long"),
                intensity=details_data.get("intensity"),
                media=media,
                episode_alias=details_data.get("episode_alias", ""),
                show_alias=details_data.get("show_alias", ""),
                broadcast=details_data.get("broadcast", ""),
                mixcloud=details_data.get("mixcloud"),
                audio_sources=audio_sources,
                brand=details_data.get("brand", {}),
                embeds=details_data.get("embeds", {}),
                links=[Link(**link) for link in details_data.get("links", [])],
            )

            # Create Embeds
            embeds = Embeds(details=details)

            broadcasts.append(
                Broadcast(
                    channel=channel["channel_name"],
                    title=html.unescape(broadcast_data["broadcast_title"]),
                    start_time=broadcast_data["start_timestamp"],
                    end_time=broadcast_data["end_timestamp"],
                    embeds=embeds,
                    links=links,
                    name=details_data.get("name"),
                    description=details_data.get("description"),
                    location_short=details_data.get("location_short"),
                    location_long=details_data.get("location_long"),
                    show_alias=details_data.get("show_alias"),
                    episode_alias=details_data.get("episode_alias"),
                    picture_url=media.picture_large,
                    raw_json=broadcast_data,
                )
            )

    return broadcasts
