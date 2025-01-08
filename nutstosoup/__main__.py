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
            channel_name = f"Channel {broadcast.channel}"
            print(f"\n{channel_name}")
            print("-" * len(channel_name))
            print(f"{broadcast.title} 🔴")
            
            details = broadcast.embeds.details
            
            if details.description:
                print(f"\n{details.description}")
            
            if details.genres:
                print("\nGenres:")
                for genre in details.genres:
                    print(f"- {genre.value}")
            
            if details.moods:
                print("\nMoods:")
                for mood in details.moods:
                    print(f"- {mood.value}")
            
            if details.location_long:
                print(f"\nLocation: {details.location_long}")
            
            if details.external_links:
                print("\nLinks:")
                for link in details.external_links:
                    print(f"- {link}")
            
            if details.audio_sources:
                print("\nAudio Sources:")
                for source in details.audio_sources:
                    print(f"- {source.source}: {source.url}")
            
            if details.mixcloud:
                print(f"\nMixcloud: {details.mixcloud}")
            
            print(f"\nStart: {broadcast.start_time}")
            print(f"End: {broadcast.end_time}")
            
            if details.media.picture_large:
                print(f"\nArtwork: {details.media.picture_large}")

        # Display mixtapes
        mixtapes = get_mixtapes()

        print("\nMixtapes")
        print("--------")
        for mixtape in mixtapes.values():
            print(f"\n{mixtape.title} ({mixtape.mixtape_alias})")
            print("-" * len(mixtape.title))
            print(f"{mixtape.subtitle}")
            print(f"\n{mixtape.description}")
            if mixtape.credits:
                print("\nFeaturing:")
                for credit in mixtape.credits[:5]:  # Show first 5 credits
                    print(f"- {credit['name']}")
                if len(mixtape.credits) > 5:
                    print(f"...and {len(mixtape.credits) - 5} more")
            print(f"\n🎵 {mixtape.stream_url}")

    except NTSAPITimeoutError:
        print("Error: Request timed out")
    except NTSAPIResponseError as e:
        print(f"Error: API returned {e.status_code}: {str(e)}")
    except NTSAPIError as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
