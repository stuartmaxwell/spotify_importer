import argparse
import csv
import os
from datetime import datetime

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials from environment variables
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = "http://localhost:8000/callback"
SCOPE = "user-library-modify"


def get_spotify_client():
    if not all([SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET]):
        raise ValueError(
            "Spotify API credentials are missing. Please check your .env file."
        )

    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=SCOPE,
        )
    )


def search_album(sp, artist, album):
    results = sp.search(q=f"artist:{artist} album:{album}", type="album")

    if results["albums"]["items"]:
        album_data = results["albums"]["items"][0]
        return {
            "found": True,
            "album_id": album_data["id"],
            "album_name": album_data["name"],
            "artist_name": album_data["artists"][0]["name"],
        }
    return {"found": False}


def get_album_tracks(sp, album_id):
    tracks = sp.album_tracks(album_id)
    return [track["id"] for track in tracks["items"]]


def add_album_to_library(sp, album_id):
    sp.current_user_saved_albums_add([album_id])


def process_album(sp, artist, album, dry_run):
    search_result = search_album(sp, artist, album)

    if search_result["found"]:
        album_id = search_result["album_id"]
        album_name = search_result["album_name"]
        artist_name = search_result["artist_name"]

        tracks = sp.album_tracks(album_id)
        track_count = len(tracks["items"])

        if dry_run:
            action = "Would add"
        else:
            add_album_to_library(sp, album_id)
            action = "Added"

        return {
            "status": "success",
            "action": action,
            "artist": artist_name,
            "album": album_name,
            "track_count": track_count,
            "spotify_id": album_id,
        }
    else:
        return {
            "status": "not_found",
            "action": "Not found",
            "artist": artist,
            "album": album,
            "track_count": 0,
            "spotify_id": "",
        }


def count_albums(root_dir):
    album_count = 0
    for artist in os.listdir(root_dir):
        artist_path = os.path.join(root_dir, artist)
        if os.path.isdir(artist_path):
            album_count += sum(
                1
                for item in os.listdir(artist_path)
                if os.path.isdir(os.path.join(artist_path, item))
            )
    return album_count


def process_music_directory(sp, root_dir, dry_run, csv_writer):
    total_albums = count_albums(root_dir)
    processed_albums = 0
    matched_albums = 0
    not_found_albums = 0

    for artist in os.listdir(root_dir):
        artist_path = os.path.join(root_dir, artist)
        if os.path.isdir(artist_path):
            for album in os.listdir(artist_path):
                album_path = os.path.join(artist_path, album)
                if os.path.isdir(album_path):
                    result = process_album(sp, artist, album, dry_run)
                    csv_writer.writerow(result)
                    processed_albums += 1
                    if result["status"] == "success":
                        matched_albums += 1
                    else:
                        not_found_albums += 1
                    print(
                        f"\rProcessed {processed_albums}/{total_albums} albums",
                        end="",
                        flush=True,
                    )

    print()  # New line after progress indicator
    return matched_albums, not_found_albums


def main():
    parser = argparse.ArgumentParser(
        description="Import local music library to Spotify"
    )
    parser.add_argument("music_dir", help="Path to your music directory")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without making changes",
    )
    args = parser.parse_args()

    try:
        sp = get_spotify_client()
    except ValueError as e:
        print(f"Error: {e}")
        return

    mode = "dry_run" if args.dry_run else "live"
    print(f"{mode.capitalize()} mode: Processing music directory...")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"spotify_import_log_{mode}_{timestamp}.csv"

    with open(log_filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "status",
            "action",
            "artist",
            "album",
            "track_count",
            "spotify_id",
        ]
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        matched_albums, not_found_albums = process_music_directory(
            sp, args.music_dir, args.dry_run, csv_writer
        )

    print(f"Log saved to {log_filename}")
    print(
        f"Summary: {matched_albums} albums matched, {not_found_albums} albums not found"
    )


if __name__ == "__main__":
    main()
