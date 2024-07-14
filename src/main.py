import logging
import os
import sys

from dotenv import load_dotenv
from pathlib import Path

from spotify import SpotifyFetcher

logging.basicConfig(
    stream=sys.stdout,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Load both .env files
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env.credentials")
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env.misc")

# Spotify Client Credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
# Spotify's current user
SPOTIFY_CURRENT_USER = os.getenv("SPOTIFY_CURRENT_USER")


def main():
    # Instantiate the fetcher
    fetcher = SpotifyFetcher(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        current_user=SPOTIFY_CURRENT_USER,
    )
    # (1) Look for playlists by name
    playlist_name_query = input("Provide a playlist (partial) name: ")
    playlists_found = fetcher.filter_playlists_by_name(playlist_name_query)

    if not playlists_found:
        logger.error("No playlists found with given name.")
        exit(0)

    logger.info(f"Found {len(playlists_found)} playlists: {[p.name for p in playlists_found]}")

    # (2) Select a playlist, retrieve all of its information and return it in our derby format
    selected_playlist = None
    while not selected_playlist:
        selected_playlist_index = input(
            "Which playlist would you like to retrieve information for? (provide list position [0-*]): "
        )
        try:
            selected_playlist = playlists_found[int(selected_playlist_index)]
        except IndexError:
            logger.error("Provide a valid position in the list.")
        except ValueError:
            logger.error("Provide a valid integer position in the list.")

    logger.info(fetcher.get_derby_entries(selected_playlist.id))


if __name__ == "__main__":
    logger.info("Starting app...")
    main()
    logger.info("Done!")
