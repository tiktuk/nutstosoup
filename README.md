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
        print(f"Now playing on Channel {broadcast['channel']}: {broadcast['title']}")
        print(f"Start time: {broadcast['start_time']}")
        print(f"End time: {broadcast['end_time']}")

    # Get all mixtapes
    mixtapes = get_mixtapes()
    
    # Print available mixtapes
    for mixtape in mixtapes.values():
        print(f"\n{mixtape['title']}")
        print(f"{mixtape['subtitle']}")
        print(f"Description: {mixtape['description']}")
        print(f"Stream URL: {mixtape['stream_url']}")
        
    # Get a specific mixtape by alias
    poolside = mixtapes.get("poolside")
    if poolside:
        print(f"\nPoolside mixtape: {poolside['title']}")
        print(f"Stream URL: {poolside['stream_url']}")

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
Start time: 2025-01-07T15:00:00Z
End time: 2025-01-07T17:00:00Z

Now playing on Channel 2: ARRHYTHMIA
Start time: 2025-01-07T14:00:00Z
End time: 2025-01-07T16:00:00Z

Poolside
Balearic, boogie, and sophisti-pop for poolsides, beaches and car stereos.
Description: Whisk yourself away with an unlimited supply of NTS' most sun-kissed mixes, crossing all borders and genres.
Stream URL: https://stream-mixtape-geo.ntslive.net/mixtape4

Slow Focus
Meditative, relaxing and beatless: ambient, drone and ragas.
Description: Tune in and zone out with NTS' compendium of the beatless and transcendental. Calming sounds to help you focus or drift away.
Stream URL: https://stream-mixtape-geo.ntslive.net/mixtape

Poolside mixtape: Poolside
Stream URL: https://stream-mixtape-geo.ntslive.net/mixtape4
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
