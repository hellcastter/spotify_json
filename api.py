import os
import json
import base64
import requests
from dotenv import load_dotenv

from pprint import pprint

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_token() -> str:
    """get spotify token

    Returns:
        str: token

    >>> isinstance(get_token, str)
    True
    """
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data, timeout=10000)
    json_result = json.loads(result.content)
    return json_result['access_token']

def get_headers(token: str) -> dict:
    """get headers

    Args:
        token (str): spotify token

    Returns:
        dict: all headers
    """
    return {"Authorization": f"Bearer {token}"}

def get(endpoint: str, query="") -> dict:
    """method to get info

    Args:
        endpoint (str): url
        query (str, optional): Defaults to "".

    Returns:
        dict: response
    """
    headers = get_headers( get_token() )

    url = endpoint + query
    response = requests.get(url, headers=headers, timeout=10000)
    return json.loads(response.content)

def search(query: str, q_type: str, limit=10):
    """search method

    Args:
        token (str): spotify token
        query (str): what to search
        q_type (str): type of search
        limit (int, optional): Defaults to 10.
    """
    endpoint = "https://api.spotify.com/v1/search"
    query = f"?q={query}&type={q_type}&limit={limit}"

    return get(endpoint, query)

def get_info(artist: dict):
    """get info about artist

    Args:
        artist (dict): artist dictionary
    """
    print(f"Name: {artist['name']}")
    print(f"Followers: {int(artist['followers']['total']):,}")
    print(f"Genres: {', '.join(artist['genres'])}")
    print(f"Popularity: {artist['popularity']}")
    print(f"URL: {artist['external_urls']['spotify']}")

def get_albums(artist_id: str):
    """get artist albums

    Args:
        artist_id (str): id of artist
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    query = "?include_groups=single,album"

    result = get(url, query)

    for idx, item in enumerate(result['items']):
        print(f"{idx + 1}. {item['name']} ({item['album_type']})")
        print(f"    Release date: {item['release_date']}")
        print(f"    Total tracks: {item['total_tracks']}")
        print(f"    URL: {item['external_urls']['spotify']}")
        print()

def convert_milliseconds(milliseconds: int) -> str:
    """convert milliseconds to minutes and seconds

    Args:
        milliseconds (int): milliseconds

    Returns:
        str: resulted string
    """
    seconds = (milliseconds // 1000) % 60
    minutes = (milliseconds // (1000 * 60)) % 60

    return f"{minutes}:{seconds}"

def get_top_songs(artist_id: str):
    """get top tracks

    Args:
        artist_id (str): artist id
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    query = "?market=UA"
    top_tracks = get(url, query)

    top_tracks = top_tracks['tracks']

    for idx, track in enumerate(top_tracks):
        print(f"{idx + 1}. {track['name']} — {convert_milliseconds(track['duration_ms'])}")
        print(f"    Album: {track['album']['name']} ({track['album']['release_date']})")
        print(f"    URL: {track['external_urls']['spotify']}")
        print()


def get_related_artists(artist_id: str):
    """get artists

    Args:
        artist_id (str): artist id
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"

    related_artists = get(url)['artists']

    for idx, artist in enumerate(related_artists):
        print(f"{idx + 1}.")
        get_info(artist)
        print()
