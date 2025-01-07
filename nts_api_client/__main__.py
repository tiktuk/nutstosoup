"""Command-line interface for NTS API client."""

from . import get_nts_live_data


def main():
    """Display currently playing shows on NTS Radio."""
    data, error = get_nts_live_data()

    if error:
        print(f"Error: {error}")
        return

    if not data or "results" not in data:
        print("Error: Invalid response from NTS API")
        return

    for channel in data["results"]:
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


if __name__ == "__main__":
    main()
