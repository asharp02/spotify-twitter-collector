import csv
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)


def handle_spotify_data(spotify_data):
    with open("spotify_data.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(spotify_data)


def get_genres():
    genres = sp.recommendation_genre_seeds()
    return genres


def get_random_search():
    chars = "abcdefghijklmnopqrstuvwxyz"
    rand_char = chars[random.randint(0, 25)]
    random_search = f"{rand_char}%"
    return random_search


def get_random_tracks_by_genre():
    genres = get_genres()["genres"]
    # print(genres)
    print(genres)
    for genre in genres:
        print(genre)
        tracks_added = []
        track_count = 0
        offset = 250
        while len(tracks_added) < 25:
            try:
                results = sp.search(
                    f"genre:{genre}", type="track", limit=50, offset=offset, market="US"
                )
            except SpotifyException:
                print(f"Could not find enough tracks for {genre}")
                break
            for item in results["tracks"]["items"]:
                popularity = item["popularity"]
                if item["id"] in tracks_added:
                    continue
                if popularity < 68:
                    track_name = item["name"]
                    artist_name = item["artists"][0]["name"]
                    track_id = item["id"]
                    album = item["album"]["name"]
                    release_date = item["album"]["release_date"]
                    data = [
                        track_id,
                        track_name,
                        artist_name,
                        album,
                        release_date,
                        popularity,
                        genre,
                    ]
                    handle_spotify_data(data)
                    tracks_added.append(track_id)
                    if len(tracks_added) >= 25:
                        break
            offset += 50


with open("spotify_data.csv", "a") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "Track ID",
            "Track Name",
            "Artist Name",
            "Album",
            "Release Date",
            "Popularity",
            "Genre",
        ]
    )
get_random_tracks_by_genre()
