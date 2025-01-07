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
