from dataclasses import dataclass
from datetime import datetime


@dataclass
class SpotifyPlaylist:
    """
    Dataclass to represent a Spotify playlist. It only includes the relevant fields for the application.

    Args:
        id (str): Spotify playlist ID.
        name (str): Spotify playlist name.
    """

    id: str
    name: str


@dataclass
class SpotifyArtist:
    """
    Dataclass to represent a Spotify artist. It includes the relevant fields for the application.

    Args:
        id (str): Spotify artist ID.
        name (str): Spotify artist name.
    """

    id: str
    name: str


@dataclass
class SpotifyTrack:
    """
    Dataclass to represent a Spotify track. It includes the relevant fields for the application.

    Args:
        id (str): Spotify track ID.
        name (str): Spotify track name.
        artists (List[SpotifyArtist]): Spotify track artists.
    """

    id: str
    name: str
    artists: list[SpotifyArtist]


@dataclass
class SpotifyUser:
    """
    Dataclass to represent a Spotify user. It includes the relevant fields for the application.

    Args:
        id (str): Spotify user ID.
        display_name (str): Spotify username.
    """

    id: str
    display_name: str


@dataclass
class SongDerbyEntry:
    """
    Dataclass to represent an entry for the game.

    Args:
        track (SpotifyTrack): Spotify track.
        added_by (SpotifyUser): Spotify user that added the track.
        added_at (datetime): When the track was added to the playlist.
    """

    track: SpotifyTrack
    added_by: SpotifyUser
    added_at: datetime
