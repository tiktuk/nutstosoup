"""Test the dataclass models."""

from nutstosoup import Broadcast, Mixtape


def test_broadcast_creation():
    """Test creating a Broadcast instance."""
    broadcast = Broadcast(
        channel="1",
        title="TED DRAWS",
        start_time="2025-01-07T15:00:00Z",
        end_time="2025-01-07T17:00:00Z",
        name="Ted Draws",
        description="Hip-hop scholar, esteemed illustrator and all round head Ted Draws holds down a killer 2 hour monthly slot on Tuesday afternoons.",
        location_short="LDN",
        location_long="London",
        show_alias="TED-DRAWS",
        episode_alias="ted-draws-7th-january-2025",
        picture_url="https://media2.ntslive.co.uk/resize/1600x1600/330d6b2a-fb0f-4a8c-bbd1-a479649510e2_1658793600.jpeg",
    )

    assert broadcast.channel == "1"
    assert broadcast.title == "TED DRAWS"
    assert broadcast.start_time == "2025-01-07T15:00:00Z"
    assert broadcast.end_time == "2025-01-07T17:00:00Z"
    assert broadcast.name == "Ted Draws"
    assert broadcast.description == "Hip-hop scholar, esteemed illustrator and all round head Ted Draws holds down a killer 2 hour monthly slot on Tuesday afternoons."
    assert broadcast.location_short == "LDN"
    assert broadcast.location_long == "London"
    assert broadcast.show_alias == "TED-DRAWS"
    assert broadcast.episode_alias == "ted-draws-7th-january-2025"
    assert broadcast.picture_url == "https://media2.ntslive.co.uk/resize/1600x1600/330d6b2a-fb0f-4a8c-bbd1-a479649510e2_1658793600.jpeg"


def test_broadcast_minimal_creation():
    """Test creating a Broadcast instance with only required fields."""
    broadcast = Broadcast(
        channel="1",
        title="TED DRAWS",
        start_time="2025-01-07T15:00:00Z",
        end_time="2025-01-07T17:00:00Z",
    )

    assert broadcast.channel == "1"
    assert broadcast.title == "TED DRAWS"
    assert broadcast.start_time == "2025-01-07T15:00:00Z"
    assert broadcast.end_time == "2025-01-07T17:00:00Z"
    assert broadcast.name is None
    assert broadcast.description is None
    assert broadcast.location_short is None
    assert broadcast.location_long is None
    assert broadcast.show_alias is None
    assert broadcast.episode_alias is None
    assert broadcast.picture_url is None
    assert broadcast.raw_json is None


def test_mixtape_creation():
    """Test creating a Mixtape instance."""
    mixtape = Mixtape(
        title="Poolside",
        subtitle="Balearic, boogie, and sophisti-pop for poolsides, beaches and car stereos.",
        description="Whisk yourself away with an unlimited supply of NTS' most sun-kissed mixes, crossing all borders and genres.",
        stream_url="https://stream-mixtape-geo.ntslive.net/mixtape4",
        mixtape_alias="poolside",
        picture_url="https://media2.ntslive.co.uk/resize/1600x1600/cf5afb01-5a68-4fa0-a1c6-415b35d09ed6_1542931200.jpeg",
        credits=[{"name": "All Styles All Smiles", "path": "/shows/all-styles-all-smiles"}],
    )

    assert mixtape.title == "Poolside"
    assert mixtape.subtitle == "Balearic, boogie, and sophisti-pop for poolsides, beaches and car stereos."
    assert mixtape.description == "Whisk yourself away with an unlimited supply of NTS' most sun-kissed mixes, crossing all borders and genres."
    assert mixtape.stream_url == "https://stream-mixtape-geo.ntslive.net/mixtape4"
    assert mixtape.mixtape_alias == "poolside"
    assert mixtape.picture_url == "https://media2.ntslive.co.uk/resize/1600x1600/cf5afb01-5a68-4fa0-a1c6-415b35d09ed6_1542931200.jpeg"
    assert mixtape.credits is not None
    assert len(mixtape.credits) == 1
    assert mixtape.credits[0]["name"] == "All Styles All Smiles"
    assert mixtape.credits[0]["path"] == "/shows/all-styles-all-smiles"


def test_mixtape_minimal_creation():
    """Test creating a Mixtape instance with only required fields."""
    mixtape = Mixtape(
        title="Poolside",
        subtitle="Balearic, boogie, and sophisti-pop for poolsides, beaches and car stereos.",
        description="Whisk yourself away with an unlimited supply of NTS' most sun-kissed mixes, crossing all borders and genres.",
        stream_url="https://stream-mixtape-geo.ntslive.net/mixtape4",
        mixtape_alias="poolside",
    )

    assert mixtape.title == "Poolside"
    assert mixtape.subtitle == "Balearic, boogie, and sophisti-pop for poolsides, beaches and car stereos."
    assert mixtape.description == "Whisk yourself away with an unlimited supply of NTS' most sun-kissed mixes, crossing all borders and genres."
    assert mixtape.stream_url == "https://stream-mixtape-geo.ntslive.net/mixtape4"
    assert mixtape.mixtape_alias == "poolside"
    assert mixtape.picture_url is None
    assert mixtape.credits is None
    assert mixtape.raw_json is None
