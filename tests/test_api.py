"""Test the NTS API client functionality."""

import json
import pytest
from requests.exceptions import Timeout, RequestException

from nutstosoup import (
    fetch_nts_api,
    get_current_broadcasts,
    get_mixtapes,
    NTSAPIError,
    NTSAPITimeoutError,
    NTSAPIResponseError,
)


def test_fetch_nts_api_timeout(monkeypatch):
    """Test handling of timeout errors."""

    def mock_get(*args, **kwargs):
        raise Timeout("Request timed out")

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(NTSAPITimeoutError) as exc_info:
        fetch_nts_api("live")
    assert str(exc_info.value) == "Request timed out"


def test_fetch_nts_api_response_error(monkeypatch):
    """Test handling of HTTP error responses."""

    class MockResponse:
        status_code = 404

        def raise_for_status(self):
            raise RequestException(f"404 Client Error: Not Found")

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(NTSAPIResponseError) as exc_info:
        fetch_nts_api("live")
    assert "404" in str(exc_info.value)


def test_get_current_broadcasts_invalid_format(monkeypatch):
    """Test handling of invalid live broadcast data format."""

    class MockResponse:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return {"invalid": "format"}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(NTSAPIError) as exc_info:
        get_current_broadcasts()
    assert str(exc_info.value) == "Invalid live data format"


def test_get_mixtapes_invalid_format(monkeypatch):
    """Test handling of invalid mixtapes data format."""

    class MockResponse:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return {"invalid": "format"}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(NTSAPIError) as exc_info:
        get_mixtapes()
    assert str(exc_info.value) == "Invalid mixtapes data format"


def test_get_current_broadcasts_success(monkeypatch):
    """Test successful parsing of live broadcast data."""
    with open("examples/api_example_live.json") as f:
        example_data = json.load(f)

    class MockResponse:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return example_data

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    broadcasts = get_current_broadcasts()
    assert len(broadcasts) == 2

    # Test Channel 1 broadcast
    assert broadcasts[0].channel == "1"
    assert broadcasts[0].title == "TED DRAWS"
    assert broadcasts[0].start_time == "2025-01-07T15:00:00Z"
    assert broadcasts[0].end_time == "2025-01-07T17:00:00Z"
    assert broadcasts[0].name == "Ted Draws"
    assert broadcasts[0].description == "Hip-hop scholar, esteemed illustrator and all round head Ted Draws holds down a killer 2 hour monthly slot on Tuesday afternoons."
    assert broadcasts[0].location_short == "LDN"
    assert broadcasts[0].location_long == "London"
    assert broadcasts[0].show_alias == "TED-DRAWS"
    assert broadcasts[0].episode_alias == "ted-draws-7th-january-2025"

    # Test Channel 2 broadcast
    assert broadcasts[1].channel == "2"
    assert broadcasts[1].title == "ARRHYTHMIA"
    assert broadcasts[1].start_time == "2025-01-07T14:00:00Z"
    assert broadcasts[1].end_time == "2025-01-07T16:00:00Z"
    assert broadcasts[1].name == "ARRHYTHMIA"
    assert broadcasts[1].description == "Broadcasting out of Birmingham, Arrhythmia is a monthly exploration of interesting new audio and abnormal rhythms. Expect irregular, dark or heavy - but not always."
    assert broadcasts[1].location_short == "BHM"
    assert broadcasts[1].location_long == "Birmingham"
    assert broadcasts[1].show_alias == "ARRHYTHMIA"
    assert broadcasts[1].episode_alias == "arrhythmia-7th-january-2025"


def test_get_mixtapes_success(monkeypatch):
    """Test successful parsing of mixtapes data."""
    with open("examples/api_example_mixtapes.json") as f:
        example_data = json.load(f)

    class MockResponse:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return example_data

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    mixtapes = get_mixtapes()
    assert len(mixtapes) > 0

    # Test first mixtape (Poolside)
    poolside = mixtapes["poolside"]
    assert poolside.title == "Poolside"
    assert poolside.subtitle == "Balearic, boogie, and sophisti-pop for poolsides, beaches and car stereos."
    assert poolside.description == "Whisk yourself away with an unlimited supply of NTS’ most sun-kissed mixes, crossing all borders and genres."
    assert poolside.stream_url == "https://stream-mixtape-geo.ntslive.net/mixtape4"
    assert poolside.mixtape_alias == "poolside"
    assert poolside.credits is not None
    assert len(poolside.credits) > 0
    assert poolside.credits[0]["name"] == "All Styles All Smiles"
    assert poolside.credits[0]["path"] == "/shows/all-styles-all-smiles"
