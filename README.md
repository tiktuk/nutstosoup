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

## Usage

```python
from nutstosoup import (
    get_nts_live_data, 
    get_nts_mixtapes_data,
    NTSAPIError,
    NTSAPITimeoutError,
    NTSAPIResponseError
)

try:
    # Get current broadcast data
    live_data = get_nts_live_data(timeout=10)  # timeout in seconds
    
    # Get current show on channel 1
    channel_1 = live_data["results"][0]
    current_show = channel_1["now"]
    print(f"Now playing on Channel 1: {current_show['broadcast_title']}")
    
    # Get show details if available
    if "details" in current_show["embeds"]:
        details = current_show["embeds"]["details"]
        print(f"Description: {details['description']}")
        print(f"Location: {details['location_long']}")
        
        # Get genres if available
        if details["genres"]:
            genres = [genre["value"] for genre in details["genres"]]
            print(f"Genres: {', '.join(genres)}")
    
    # Get upcoming shows
    next_show = channel_1["next"]
    print(f"\nUp next: {next_show['broadcast_title']}")
    print(f"Starts at: {next_show['start_timestamp']}")

    # Get mixtapes data
    mixtapes_data = get_nts_mixtapes_data()
    # Print available mixtape streams
    for mixtape in mixtapes_data["results"]:
        print(f"\n{mixtape['title']}")
        print(f"Description: {mixtape['description']}")
        print(f"Stream URL: {mixtape['audio_stream_endpoint']}")

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
Genres: Gangsta Rap, Classic Hip Hop, Hip Hop

Up next: QUEST NO MORE W/ ELHEIST
Starts at: 2025-01-07T17:00:00Z

Poolside
Description: Balearic, boogie, and sophisti-pop for poolsides, beaches and car stereos.
Stream URL: https://stream-mixtape-geo.ntslive.net/mixtape4

Slow Focus
Description: Meditative, relaxing and beatless: ambient, drone and ragas.
Stream URL: https://stream-mixtape-geo.ntslive.net/mixtape
```

## Simple Test CLI

You can test it's working by running:

```bash
    python3 -m nutstosoup
```

It should print out the current live data and mixtapes data:

```
Live Channels
-------------

Channel 1
---------
TED DRAWS 🔴
London

Hip-hop scholar, esteemed illustrator and all round head Ted Draws holds down a killer 2 hour monthly slot on Tuesday afternoons.

Gangsta Rap, Classic Hip Hop, Hip Hop 

Channel 2
---------
ARRHYTHMIA 🔴
Birmingham

Broadcasting out of Birmingham, Arrhythmia is a monthly exploration of interesting new audio and abnormal rhythms. Expect irregular, dark or heavy - but not always.

Mixtapes
--------

Poolside
--------
Balearic, boogie, and sophisti-pop for poolsides, beaches and car stereos.

Whisk yourself away with an unlimited supply of NTS’ most sun-kissed mixes, crossing all borders and genres.

🎵 https://stream-mixtape-geo.ntslive.net/mixtape4

Slow Focus
----------
Meditative, relaxing and beatless: ambient, drone and ragas.

Tune in and zone out with NTS’ compendium of the beatless and transcendental. Calming sounds to help you focus or drift away.

🎵 https://stream-mixtape-geo.ntslive.net/mixtape

Low Key
-------
Keeping it simple with lo-fi hip-hop and smooth R’n’B.

Covering everything chill – whether that’s downtempo beats, Golden Age hip-hop or grown ‘n’ sexy slow jams.

🎵 https://stream-mixtape-geo.ntslive.net/mixtape2

Memory Lane
-----------
Turn on, tune in, drop out.

Turn back the clock and lose yourself in a world of counter-cultural folk, LSD-laced psychedelia, sweet soul and raw garage rock.

🎵 https://stream-mixtape-geo.ntslive.net/mixtape6

...
```
