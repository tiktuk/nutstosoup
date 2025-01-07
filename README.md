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
class Broadcast:
    channel: str               # Channel name (e.g. "1", "2")
    title: str                 # Broadcast title
    start_time: str            # Start timestamp
    end_time: str              # End timestamp
    name: str | None           # Show name (optional)
    description: str | None    # Show description (optional)
    location_short: str | None  # Short location code (optional)
    location_long: str | None   # Full location name (optional)
    show_alias: str | None     # Show alias for URLs (optional)
    episode_alias: str | None  # Episode alias for URLs (optional)
    picture_url: str | None    # Show artwork URL (optional)
    raw_json: Dict[str, Any] | None  # Original API response data (optional)
```

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
    
    # Print current shows
    for broadcast in broadcasts:
        print(f"Now playing on Channel {broadcast.channel}: {broadcast.title}")
        if broadcast.description:
            print(f"Description: {broadcast.description}")
        if broadcast.location_long:
            print(f"Location: {broadcast.location_long}")
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
