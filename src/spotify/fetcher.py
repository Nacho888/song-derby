from dacite import from_dict as init_dataclass_from_dict
from datetime import datetime
from rapidfuzz import fuzz
from rapidfuzz.utils import default_process
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from .datamodels import SpotifyPlaylist, SpotifyTrack, SpotifyUser, SongDerbyEntry


class SpotifyFetcher:
    def __init__(self, client_id: str, client_secret: str, current_user: str):
        # Spotify's API Client Credentials to be used for AUTH token generation (handled by `spotipy`)
        self.client_id = client_id
        self.client_secret = client_secret

        # The fetcher is couples to a specific user
        self.current_user = current_user

        # Instantiate the client for all underlying operations in the class
        self.client = Spotify(
            auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        )

    def get_playlists(self) -> list[SpotifyPlaylist]:
        """
        Fetches playlists from the current user and converts them into `SpotifyPlaylist` objects.

        Returns: list[SpotifyPlaylist]
        """
        playlists = self.client.user_playlists(user=self.current_user)
        return [
            init_dataclass_from_dict(data_class=SpotifyPlaylist, data=item)
            for item in playlists["items"]
        ]

    def get_user_by_id(self, user_id: str) -> SpotifyUser:
        """
        Given a Spotify user id, parses it into a `SpotifyUser` object.

        Args:
            user_id (str): Spotify user id.

        Returns: SpotifyUser.
        """
        return init_dataclass_from_dict(data_class=SpotifyUser, data=self.client.user(user=user_id))

    def get_derby_entries(self, playlist_id: str) -> list[SongDerbyEntry]:
        """
        Retrieves all tracks from a playlist and converts them into `SongDerbyEntry` objects. This process involves
        processing each track and extract the necessary information from it (`SpotifyTrack`, `SpotifyUser` and
        'added_at') in order to create a `SongDerbyEntry` object.

        Args:
            playlist_id (str): Spotify playlist id.

        Returns: list[SongDerbyEntry]: The processed entries from a playlist in the derby format.
        """
        tracks = self.client.playlist_items(playlist_id=playlist_id, additional_types="track")
        entries = []
        for track in tracks["items"]:
            entry = {
                "track": init_dataclass_from_dict(data_class=SpotifyTrack, data=track["track"]),
                "added_by": self.get_user_by_id(track["added_by"]["id"]),
                "added_at": datetime.strptime(track["added_at"], "%Y-%m-%dT%H:%M:%SZ"),
            }
            entries.append(entry)
        return [
            init_dataclass_from_dict(data_class=SongDerbyEntry, data=entry) for entry in entries
        ]

    def filter_playlists_by_name(
        self, name_query: str, fuzzy_ratio_threshold: float = 75.0
    ) -> list[SpotifyPlaylist]:
        """
        Filters playlists by name. Applies fuzzy search using the `name_query` string provided against the names of the
        playlists returned by `get_playlists`.

        Applies the normalized Indel distance (as a ratio) using the set of tokens (unique and common words) in the
        strings: https://rapidfuzz.github.io/RapidFuzz/Usage/fuzz.html#rapidfuzz.fuzz.token_set_ratio

        Furthermore, the strings in the query are preprocessed as:

        - Remove all non-alphanumeric characters
        - Trim whitespaces
        - Convert to lowercase

        It will only return those playlists whose names match `name_query` with a certainty ratio of at least
        `fuzzy_ratio_threshold` [0.0-100.0] (least to most similar).

        Args:
            name_query (str): Name of the playlist to use as query.
            fuzzy_ratio_threshold (float): The ratio that controls how similar the fuzzy search results should be
                to be considered a match. It ranges between 0.0 and 100.0 inclusive (least to most similar). Defaults
                to 75.0.

        Returns: list[SpotifyPlaylist]: The playlists whose names match `name_query` following the specified fuzzy
            search rules.
        """
        playlists = self.get_playlists()
        return [
            p
            for p in playlists
            if fuzz.token_set_ratio(p.name, name_query, processor=default_process)
            >= fuzzy_ratio_threshold
        ]
