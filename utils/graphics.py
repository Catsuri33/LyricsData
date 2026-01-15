import matplotlib.pyplot as plt
import pandas as pd
import json
from config import GRAPHICS_FOLDER

def get_data(src_root: Path):
    summary_root = src_root / "global.json"
    root_content = None
    artists_content = {}
    albums_content = {}
    
    root_content = load_summary_content(summary_root)

    for artist_dir in src_root.iterdir():
        if not artist_dir.is_dir():
            continue
        artist_name = artist_dir.name
        summary_artist = artist_dir / "summary.json"

        artists_content[artist_name] = load_summary_content(summary_artist)

        for album_dir in artist_dir.iterdir():
            if not album_dir.is_dir():
                continue
            album_name = album_dir.name
            album_key = (artist_name, album_name)
            summary_album = album_dir / "summary.json"

            albums_content[album_name] = load_summary_content(summary_album)

    return root_content, artists_content, albums_content

def generate_graphics(src_root: Path, min_height: int = None):
    root_content, artists_content, albums_content = get_data(src_root)

    generate_graphic(root_content, 80, "global.png")
    
    for artist_name in artists_content:
        artist_obj = artists_content[artist_name]
        generate_graphic(artist_obj, min_height, artist_name.replace(" ", "_") + "_summary.png", artist_name)

    # TODO Albums

def load_summary_content(path: Path):
    with path.open(encoding="utf-8") as fp:
        data = json.load(fp)
    return data

def generate_graphic(json_obj, min_height: int = None, name: str = "summary.png", graphic_name: str = "Global"):
    df = pd.DataFrame(list(json_obj.items()), columns=["mot", "occurrences"])
    df = df.sort_values(by="occurrences", ascending=False)

    if min_height is None:
        df = df.copy()
    else:
        df = df[df["occurrences"] >= min_height]

    if not df.empty:
        plt.figure(figsize=(12, 6))
        bars = plt.bar(df["mot"], df["occurrences"], color="#4A90E2")
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2,
                    height + 1,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10, rotation=45)

        plt.title("Occurrences de chaque mot pour " + graphic_name)
        plt.xlabel("Mot")
        plt.ylabel("Nombre d'occurrences")
        plt.xticks(rotation=90, fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        save_path = GRAPHICS_FOLDER + "/" + name
        plt.savefig(save_path)
