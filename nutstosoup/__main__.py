"""Command-line interface for NTS API client."""

from . import (
    get_current_broadcasts,
    get_mixtapes,
    NTSAPIError,
    NTSAPITimeoutError,
    NTSAPIResponseError,
)


def main():
    """Display currently playing shows and mixtapes on NTS Radio."""
    try:
        # Display live channels
        broadcasts = get_current_broadcasts()

        print("Live Channels")
        print("-------------")
        for broadcast in broadcasts:
            channel_name = f"Channel {broadcast.get('channel')}"
            print(f"\n{channel_name}")
            print("-" * len(channel_name))
            print(f"{broadcast.get('title')} 🔴")
            print(f"Start: {broadcast.get('start_time')}")
            print(f"End: {broadcast.get('end_time')}")

        # Display mixtapes
        mixtapes = get_mixtapes()

        print("\nMixtapes")
        print("--------")
        for mixtape in mixtapes.values():
            print(f"\n{mixtape.get('title')}")
            print("-" * len(mixtape.get("title", "")))
            print(f"{mixtape.get('subtitle')}")
            print(f"\n{mixtape.get('description')}")
            print(f"\n🎵 {mixtape.get('stream_url')}")

    except NTSAPITimeoutError:
        print("Error: Request timed out")
    except NTSAPIResponseError as e:
        print(f"Error: API returned {e.status_code}: {str(e)}")
    except NTSAPIError as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
