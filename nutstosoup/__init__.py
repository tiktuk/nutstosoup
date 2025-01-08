"""Module for interacting with the NTS Radio API."""

import html
import requests
from dataclasses import dataclass
from typing import Dict, Any, List
from requests.exceptions import RequestException, Timeout


@dataclass
class BroadcastMedia:
    """Represents media URLs for a broadcast."""

    background_large: str | None = None
    background_medium_large: str | None = None
    background_medium: str | None = None
    background_small: str | None = None
    background_thumb: str | None = None
    picture_large: str | None = None
    picture_medium_large: str | None = None
    picture_medium: str | None = None
    picture_small: str | None = None
    picture_thumb: str | None = None


@dataclass
class Link:
    """Represents a link in the API response."""

    rel: str
    href: str
    type: str


@dataclass
class AudioSource:
    """Represents an audio source."""

    url: str
    source: str


@dataclass
class Genre:
    """Represents a genre."""

    id: str
    value: str


@dataclass
class Mood:
    """Represents a mood."""

    id: str
    value: str


@dataclass
class Details:
    """Represents the detailed information about a broadcast."""

    status: str
    updated: str
    name: str
    description: str
    description_html: str
    external_links: List[str]
    moods: List[Mood]
    genres: List[Genre]
    location_short: str | None
    location_long: str | None
    intensity: str | None
    media: BroadcastMedia
    episode_alias: str
    show_alias: str
    broadcast: str
    mixcloud: str | None
    audio_sources: List[AudioSource]
    brand: Dict[str, Any]
    embeds: Dict[str, Any]
    links: List[Link]


@dataclass
class Embeds:
    """Represents the embeds section of a broadcast."""

    details: Details


@dataclass
class Broadcast:
    """Represents a live broadcast on an NTS channel."""

    channel: str
    title: str
    start_time: str
    end_time: str
    embeds: Embeds
    links: List[Link]
    name: str | None = None
    description: str | None = None
    location_short: str | None = None
    location_long: str | None = None
    show_alias: str | None = None
    episode_alias: str | None = None
    picture_url: str | None = None
    raw_json: Dict[str, Any] | None = None


@dataclass
class MixtapeMedia:
    """Represents media URLs for a mixtape."""
    animation_large_landscape: str | None = None
    animation_large_portrait: str | None = None
    animation_thumb: str | None = None
    icon_black: str | None = None
    icon_white: str | None = None
    picture_large: str | None = None
    picture_medium_large: str | None = None
    picture_medium: str | None = None
    picture_small: str | None = None
    picture_thumb: str | None = None


@dataclass
class MixtapeCredit:
    """Represents a credit in a mixtape."""
    name: str
    path: str


@dataclass
class MixtapeMetadata:
    """Represents mixtape list metadata."""
    subtitle: str
    credits: str
    mq_host: str
    animation_large_portrait: str


@dataclass
class Mixtape:
    """Represents an NTS mixtape."""
    mixtape_alias: str
    title: str
    subtitle: str
    description: str
    description_html: str
    audio_stream_endpoint: str
    credits: List[MixtapeCredit]
    media: MixtapeMedia
    now_playing_topic: str
    links: List[Link]
    raw_json: Dict[str, Any] | None = None


@dataclass
class MixtapeList:
    """Represents a list of mixtapes with metadata."""
    metadata: MixtapeMetadata
    results: List[Mixtape]
    links: List[Link]


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
