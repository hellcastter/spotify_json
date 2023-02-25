""" App to work with Spotify API """
import argparse

from api import search, get_albums, get_info, get_top_songs, get_related_artists

def main():
    """ main function """
    parser = argparse.ArgumentParser(
        prog = 'Spotify JSON',
        description = 'Get info about artist so quickly. Write name and interested parameter.'
    )

    parser.add_argument('name', help="Name of artist")
    parser.add_argument('-a', '--albums', action='store_true', help="Get artist's albums.")
    parser.add_argument('-r', '--related', action='store_true', help="Get related artist.")
    parser.add_argument('-t', '--top', action='store_true', help="Get top tracks")
    parser.add_argument('-i', '--info', action='store_true', help="Get info about artist")

    args = parser.parse_args()
    name = args.name
    info = args.info
    albums = args.albums
    top = args.top
    related = args.related

    artist = search(name, 'artist', 1)

    artist_info = artist['artists']['items'][0]
    artist_id = artist_info['id']

    if info:
        get_info(artist_info)
        print()

    if albums:
        get_albums(artist_id)
        print()

    if top:
        get_top_songs(artist_id)
        print()

    if related:
        get_related_artists(artist_id)
        print()

if __name__ == "__main__":
    main()
