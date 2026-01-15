import argparse
import sys
from pathlib import Path
import os
import shutil
from colorama import Fore, Style, init as colorama_init

from config import SAVE_FOLDER, RESULT_FOLDER, GRAPHICS_FOLDER
from utils.menus import download_menu
from utils.stats_lyrics import count_occurrences, dump_results
from utils.graphics import generate_graphics

colorama_init(autoreset=True)

def build_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="lyricsdata",
        description="download lyrics and create stats on words count",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download lyrics.",
    )

    parser.add_argument(
        "-c",
        "--clear",
        action="store_true",
        help="Clear stored lyrics.",
    )

    return parser

def clean_directory(path_str: str) -> None:
    path = Path(path_str)
    if not path.is_dir():
        raise NotADirectoryError(f"{path} n'est pas un répertoire")

    for entry in path.iterdir():
        if entry.is_dir():
            shutil.rmtree(entry)
        else:
            entry.unlink()

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    os.makedirs(SAVE_FOLDER, exist_ok=True)
    os.makedirs(RESULT_FOLDER, exist_ok=True)

    if args.clear:
        clean_directory(SAVE_FOLDER)
        clean_directory(RESULT_FOLDER)
        clean_directory(GRAPHICS_FOLDER)

    if args.download:
        end = False

        while not end:
            download_menu()

        sys.exit(0)

    global_cnt, artist_cnts, album_cnts = count_occurrences(Path(SAVE_FOLDER).resolve())
    dump_results(Path(RESULT_FOLDER).resolve(), global_cnt, artist_cnts, album_cnts)
    print(f"{Fore.GREEN}\n✅  Statistiques d'occurrences générées")

    generate_graphics(Path("./results").resolve(), 40)
    print(f"{Fore.GREEN}\n✅  Graphiques générés")

if __name__ == "__main__":
    main()
