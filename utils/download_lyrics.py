import requests
import os

from config import SAVE_FOLDER, API_GET_URL

def get_lyrics(artist: str, track: str|None = None, album: str|None = None) -> str:
    if artist is None:
        raise ValueError("Missing artist name")
    
    params = {"artist_name": artist}
    if track is not None:
        params["track_name"] = track
    if album is not None:
        params["album_name"] = album
    
    response = requests.get(
        API_GET_URL,
        params=params
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Could not find lyrics for these parameters")
    
def download_lyrics(artist: str, track: str|None = None, album: str|None = None) -> None:
    json_data = get_lyrics(artist, track, album)

    for object in json_data:
        extract_title = object["name"]
        extract_album = object["albumName"]
        extract_lyrics_plain = object["plainLyrics"]
        extract_artist = object["artistName"]

        folder_path = os.path.join(SAVE_FOLDER, extract_artist, extract_album)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(SAVE_FOLDER, extract_artist, extract_album, extract_title+'.txt')
        print(file_path)
        with open(file_path, mode="w", encoding="utf-8") as f:
            f.write(extract_lyrics_plain)
