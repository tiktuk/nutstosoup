# NTS API Client

A Python client for interacting with the NTS Radio API.

## Installation

```bash
uv pip install nts-api-client
```

## Usage

```python
from nts_api_client import get_nts_live_data, get_nts_mixtapes_data

# Get current broadcast data
live_data, error = get_nts_live_data()
if error:
    print(f"Error: {error}")
else:
    print(live_data)

# Get mixtapes data
mixtapes_data, error = get_nts_mixtapes_data()
if error:
    print(f"Error: {error}")
else:
    print(mixtapes_data)
```

## Simple Test CLI

You can test it's working by running:

```bash
    python3 -m nts_api_client
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
