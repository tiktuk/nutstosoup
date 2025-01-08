# Nuts to Soup

A Python client for interacting with the NTS Radio API.

## Installation

```bash
uv add nutstosoup
```

or

```bash
pip3 install nutstosoup
```

## Error Handling

The library uses exceptions to handle errors:

- `NTSAPIError`: Base exception for all API-related errors
- `NTSAPIResponseError`: Raised when the API returns an unsuccessful status code (includes status_code attribute)
- `NTSAPITimeoutError`: Raised when the request times out

All functions accept an optional `timeout` parameter (in seconds, defaults to 10) to configure request timeouts.

## Data Classes

The library provides two dataclasses for working with NTS data:

### Broadcast

Represents a live broadcast on an NTS channel:

```python
@dataclass
class Media:
    """Media URLs for a broadcast."""
    background_large: str | None         # Large background image
    background_medium_large: str | None  # Medium-large background
    background_medium: str | None        # Medium background
    background_small: str | None         # Small background
    background_thumb: str | None         # Thumbnail background
    picture_large: str | None            # Large picture
    picture_medium_large: str | None     # Medium-large picture
    picture_medium: str | None           # Medium picture
    picture_small: str | None            # Small picture
    picture_thumb: str | None            # Thumbnail picture

@dataclass
class Link:
    """API link with relation and type."""
    rel: str                   # Link relation
    href: str                  # Link URL
    type: str                  # Content type

@dataclass
class AudioSource:
    """Audio stream source."""
    url: str                   # Stream URL
    source: str                # Source platform

@dataclass
class Genre:
    """Show genre."""
    id: str                    # Genre ID
    value: str                 # Genre name

@dataclass
class Mood:
    """Show mood."""
    id: str                    # Mood ID
    value: str                 # Mood name

@dataclass
class Details:
    """Detailed broadcast information."""
    status: str                # Publication status
    updated: str               # Last update time
    name: str                  # Show name
    description: str           # Show description
    description_html: str      # HTML description
    external_links: List[str]  # External URLs
    moods: List[Mood]         # Show moods
    genres: List[Genre]       # Show genres
    location_short: str | None # Short location
    location_long: str | None  # Full location
    intensity: str | None      # Show intensity
    media: Media              # Media URLs
    episode_alias: str        # Episode URL alias
    show_alias: str           # Show URL alias
    broadcast: str            # Broadcast time
    mixcloud: str | None      # Mixcloud URL
    audio_sources: List[AudioSource]  # Audio streams
    brand: Dict[str, Any]     # Brand info
    embeds: Dict[str, Any]    # Embedded content
    links: List[Link]         # API links

@dataclass
class Embeds:
    """Embedded content container."""
    details: Details          # Show details

@dataclass
class Broadcast:
    """Live broadcast on an NTS channel."""
    channel: str              # Channel name (e.g. "1", "2")
    title: str               # Broadcast title
    start_time: str          # Start timestamp
    end_time: str            # End timestamp
    embeds: Embeds           # Embedded content
    links: List[Link]        # API links
    name: str | None = None           # Show name (optional)
    description: str | None = None    # Show description (optional)
    location_short: str | None = None # Short location code (optional)
    location_long: str | None = None  # Full location name (optional)
    show_alias: str | None = None    # Show alias for URLs (optional)
    episode_alias: str | None = None # Episode alias for URLs (optional)
    picture_url: str | None = None   # Show artwork URL (optional)
    raw_json: Dict[str, Any] | None = None  # Original API response data
```

Example of the json of a broadcast:

```json
{
    "broadcast_title": "CALM ROOTS W/ ALEX RITA LONDON (R)",
    "start_timestamp": "2024-12-30T08:00:00Z",
    "end_timestamp": "2024-12-30T10:00:00Z",
    "embeds": {
        "details": {
            "status": "published",
            "updated": "2024-07-23T09:25:30+00:00",
            "name": "Calm Roots w/ Alex Rita",
            "description": "Hypnotic & meditative sounds from Touching Bass' Alex Rita.",
            "description_html": "<h3>Hypnotic & meditative sounds from Touching Bass' Alex Rita.</h3>",
            "external_links": [
                "https://en-gb.facebook.com/alexritaa/",
                "https://soundcloud.com/alexrita"
            ],
            "moods": [
                {
                    "id": "moods-the-healing-place",
                    "value": "The Healing Place"
                }
            ],
            "genres": [
                {
                    "id": "genres-jazz-ambientjazz",
                    "value": "Ambient Jazz"
                },
                {
                    "id": "genres-ambientnewage-ambient",
                    "value": "Ambient"
                }
            ],
            "location_short": "LDN",
            "location_long": "London",
            "intensity": null,
            "media": {
                "background_large": "https://media2.ntslive.co.uk/resize/1600x1600/d0faf1f8-0daa-486f-bbcd-607f6b0f4331_1570406400.png",
                "background_medium_large": "https://media2.ntslive.co.uk/resize/800x800/d0faf1f8-0daa-486f-bbcd-607f6b0f4331_1570406400.png",
                "background_medium": "https://media.ntslive.co.uk/resize/400x400/d0faf1f8-0daa-486f-bbcd-607f6b0f4331_1570406400.png",
                "background_small": "https://media3.ntslive.co.uk/resize/200x200/d0faf1f8-0daa-486f-bbcd-607f6b0f4331_1570406400.png",
                "background_thumb": "https://media3.ntslive.co.uk/resize/100x100/d0faf1f8-0daa-486f-bbcd-607f6b0f4331_1570406400.png",
                "picture_large": "https://media2.ntslive.co.uk/resize/1600x1600/d0faf1f8-0daa-486f-bbcd-607f6b0f4331_1570406400.png",
                "picture_medium_large": "https://media2.ntslive.co.uk/resize/800x800/d0faf1f8-0daa-486f-bbcd-607f6b0f4331_1570406400.png",
                "picture_medium": "https://media.ntslive.co.uk/resize/400x400/d0faf1f8-0daa-486f-bbcd-607f6b0f4331_1570406400.png",
                "picture_small": "https://media3.ntslive.co.uk/resize/200x200/d0faf1f8-0daa-486f-bbcd-607f6b0f4331_1570406400.png",
                "picture_thumb": "https://media3.ntslive.co.uk/resize/100x100/d0faf1f8-0daa-486f-bbcd-607f6b0f4331_1570406400.png"
            },
            "episode_alias": "calm-roots-22nd-july-2024",
            "show_alias": "calm-roots",
            "broadcast": "2024-07-22T19:00:00+00:00",
            "mixcloud": "https://www.mixcloud.com/NTSRadio/calm-roots-w-alex-rita-22nd-july-2024/",
            "audio_sources": [
                {
                    "url": "https://soundcloud.com/user-643553014/calm-roots-w-alex-rita-220724",
                    "source": "soundcloud"
                }
            ],
            "brand": {},
            "embeds": {},
            "links": [
                {
                    "rel": "self",
                    "href": "https://www.nts.live/api/v2/shows/calm-roots/episodes/calm-roots-22nd-july-2024",
                    "type": "application/vnd.episode+json;charset=utf-8"
                },
                {
                    "rel": "show",
                    "href": "https://www.nts.live/api/v2/shows/calm-roots",
                    "type": "application/vnd.show+json;charset=utf-8"
                },
                {
                    "rel": "tracklist",
                    "href": "https://www.nts.live/api/v2/shows/calm-roots/episodes/calm-roots-22nd-july-2024/tracklist",
                    "type": "application/vnd.track-list+json;charset=utf-8"
                }
            ]
        }
    },
    "links": [
        {
            "href": "https://www.nts.live/api/v2/shows/calm-roots/episodes/calm-roots-22nd-july-2024",
            "rel": "details",
            "type": "application/vnd.episode+json;charset=utf-8"
        }
    ]
}
```

There's a full example of broadcast json in the `examples` directory.

### Mixtape

Represents an NTS mixtape:

```python
@dataclass
class Mixtape:
    title: str               # Mixtape title
    subtitle: str            # Short description
    description: str         # Full description
    stream_url: str          # Audio stream URL
    mixtape_alias: str       # Mixtape alias for URLs
    picture_url: str | None  # Artwork URL (optional)
    credits: list[dict[str, str]] | None  # Contributing shows (optional)
    raw_json: Dict[str, Any] | None  # Original API response data (optional)
```

There's an example of mixtape json in the `examples` directory.

## Usage

```python
from nutstosoup import (
    get_current_broadcasts,
    get_mixtapes,
    NTSAPIError,
    NTSAPITimeoutError,
    NTSAPIResponseError
)

try:
    # Get current broadcasts for both channels
    broadcasts = get_current_broadcasts(timeout=10)  # timeout in seconds
    
    # Print current shows with detailed information
    for broadcast in broadcasts:
        print(f"Now playing on Channel {broadcast.channel}: {broadcast.title}")
        
        # Access nested details through the embeds structure
        details = broadcast.embeds.details
        
        if details.description:
            print(f"Description: {details.description}")
        
        if details.genres:
            print("Genres:")
            for genre in details.genres:
                print(f"- {genre.value}")
                
        if details.moods:
            print("Moods:")
            for mood in details.moods:
                print(f"- {mood.value}")
                
        if details.location_long:
            print(f"Location: {details.location_long}")
            
        if details.audio_sources:
            print("Audio Sources:")
            for source in details.audio_sources:
                print(f"- {source.source}: {source.url}")
                
        if details.mixcloud:
            print(f"Mixcloud: {details.mixcloud}")
            
        if details.media.picture_large:
            print(f"Artwork: {details.media.picture_large}")
            
        print(f"Start time: {broadcast.start_time}")
        print(f"End time: {broadcast.end_time}")

    # Get all mixtapes
    mixtapes = get_mixtapes()
    
    # Print available mixtapes
    for mixtape in mixtapes.values():
        print(f"\n{mixtape.title}")
        print(f"{mixtape.subtitle}")
        print(f"Description: {mixtape.description}")
        if mixtape.credits:
            print("\nFeaturing:")
            for credit in mixtape.credits[:5]:
                print(f"- {credit['name']}")
            if len(mixtape.credits) > 5:
                print(f"...and {len(mixtape.credits) - 5} more")
        print(f"Stream URL: {mixtape.stream_url}")
        
        # Access additional fields from the raw API response
        if mixtape.raw_json and "some_extra_field" in mixtape.raw_json:
            print(f"Extra field: {mixtape.raw_json['some_extra_field']}")
        
    # Get a specific mixtape by alias
    poolside = mixtapes.get("poolside")
    if poolside:
        print(f"\nPoolside mixtape: {poolside.title}")
        print(f"Stream URL: {poolside.stream_url}")

except NTSAPITimeoutError:
    print("Request timed out")
except NTSAPIResponseError as e:
    print(f"API error {e.status_code}: {str(e)}")
except NTSAPIError as e:
    print(f"API error: {str(e)}")
```

Example output:
```
Now playing on Channel 1: TED DRAWS
Description: Hip-hop scholar, esteemed illustrator and all round head Ted Draws holds down a killer 2 hour monthly slot on Tuesday afternoons.
Location: London
Start time: 2025-01-07T15:00:00Z
End time: 2025-01-07T17:00:00Z

Now playing on Channel 2: ARRHYTHMIA
Description: Broadcasting out of Birmingham, Arrhythmia is a monthly exploration of interesting new audio and abnormal rhythms. Expect irregular, dark or heavy - but not always.
Location: Birmingham
Start time: 2025-01-07T14:00:00Z
End time: 2025-01-07T16:00:00Z

Poolside (poolside)
Balearic, boogie, and sophisti-pop for poolsides, beaches and car stereos.
Description: Whisk yourself away with an unlimited supply of NTS' most sun-kissed mixes, crossing all borders and genres.

Featuring:
- All Styles All Smiles
- Altered Soul Experiment w/ Amila
- Benedek
- Braindead
- Bullion
...and 29 more

Stream URL: https://stream-mixtape-geo.ntslive.net/mixtape4

Slow Focus (slow-focus)
Meditative, relaxing and beatless: ambient, drone and ragas.
Description: Tune in and zone out with NTS' compendium of the beatless and transcendental. Calming sounds to help you focus or drift away.

Featuring:
- Aboutface
- Are You Before
- Carolina Soul
- Caterina Barbieri & Ruben Spini
- Constellation Tatsu
...and 30 more

Stream URL: https://stream-mixtape-geo.ntslive.net/mixtape

Poolside mixtape: Poolside
Stream URL: https://stream-mixtape-geo.ntslive.net/mixtape4
```

## Simple Test CLI

You can test it's working by running:

```bash
python3 -m nutstosoup
```

It will display current live broadcasts and available mixtapes with rich information including descriptions, locations, and contributing shows.
