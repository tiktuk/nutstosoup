"""Command-line interface for NTS API client."""

from . import (
    get_nts_live_data,
    get_nts_mixtapes_data,
    NTSAPIError,
    NTSAPITimeoutError,
    NTSAPIResponseError,
)


def main():
    """Display currently playing shows and mixtapes on NTS Radio."""
    try:
        # Display live channels
        live_data = get_nts_live_data()
        
        if not live_data or "results" not in live_data:
            print("Error: Invalid response from NTS Live API")
            return

        print("Live Channels")
        print("-------------")
        for channel in live_data["results"]:
            channel_name = f"Channel {channel['channel_name']}"
            print(f"\n{channel_name}")
            print("-" * len(channel_name))

            now = channel.get("now")
            if now:
                print(f"{now['broadcast_title']} 🔴")

                details = now.get("embeds", {}).get("details", {})
                if details:
                    if "location_long" in details:
                        print(f"{details['location_long']}")
                    if "description" in details:
                        print(f"\n{details['description']}")
                    if "genres" in details and details["genres"]:
                        genres = [g["value"] for g in details["genres"]]
                        if genres:
                            print(f"\n{', '.join(genres)}")

        # Display mixtapes
        mixtapes_data = get_nts_mixtapes_data()
        
        if not mixtapes_data or "results" not in mixtapes_data:
            print("\nError: Invalid response from NTS Mixtapes API")
            return

        print("\nMixtapes")
        print("--------")
        for mixtape in mixtapes_data["results"]:
            print(f"\n{mixtape['title']}")
            print("-" * len(mixtape['title']))
            if mixtape.get("subtitle"):
                print(f"{mixtape['subtitle']}")
            if mixtape.get("description"):
                print(f"\n{mixtape['description']}")
            if mixtape.get("audio_stream_endpoint"):
                print(f"\n🎵 {mixtape['audio_stream_endpoint']}")

    except NTSAPITimeoutError:
        print("Error: Request timed out")
    except NTSAPIResponseError as e:
        print(f"Error: API returned {e.status_code}: {str(e)}")
    except NTSAPIError as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
