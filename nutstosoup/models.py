"""Data models for NTS Radio API responses."""

from dataclasses import dataclass
from typing import Dict, Any, List


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
