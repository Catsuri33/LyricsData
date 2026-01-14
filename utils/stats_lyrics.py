import json
import re
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, Tuple

WORD_RE = re.compile(r"\b\w+\b", flags=re.UNICODE)

def tokenize(text: str) -> Iterable[str]:
    return (m.group(0).lower() for m in WORD_RE.finditer(text))

def count_words_in_file(file_path: Path) -> Counter:
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = file_path.read_bytes().decode(errors="ignore")
    return Counter(tokenize(content))

def merge_counters(a: Counter, b: Counter) -> Counter:
    a.update(b)
    return a

def count_occurrences(src_root: Path) -> Tuple[Counter, Dict[str, Counter], Dict[Tuple[str, str], Counter]]:
    global_counter = Counter()
    artist_counters: Dict[str, Counter] = {}
    album_counters: Dict[Tuple[str, str], Counter] = {}

    for artist_dir in src_root.iterdir():
        if not artist_dir.is_dir():
            continue
        artist_name = artist_dir.name
        artist_counters.setdefault(artist_name, Counter())

        for album_dir in artist_dir.iterdir():
            if not album_dir.is_dir():
                continue
            album_name = album_dir.name
            album_key = (artist_name, album_name)
            album_counters.setdefault(album_key, Counter())

            for txt_file in album_dir.glob("*.txt"):
                file_counter = count_words_in_file(txt_file)

                global_counter = merge_counters(global_counter, file_counter)
                artist_counters[artist_name] = merge_counters(artist_counters[artist_name], file_counter)
                album_counters[album_key] = merge_counters(album_counters[album_key], file_counter)

    return global_counter, artist_counters, album_counters

def write_counter(counter: Counter, dst_path: Path) -> None:
    sorted_items = dict(counter.most_common())
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_text(json.dumps(sorted_items, ensure_ascii=False, indent=2), encoding="utf-8")

def dump_results(
    dst_root: Path,
    global_counter: Counter,
    artist_counters: Dict[str, Counter],
    album_counters: Dict[Tuple[str, str], Counter],
) -> None:
    write_counter(global_counter, dst_root / "global.json")

    for artist, cnt in artist_counters.items():
        artist_dir = dst_root / artist
        write_counter(cnt, artist_dir / "summary.json")

    for (artist, album), cnt in album_counters.items():
        album_dir = dst_root / artist / album
        write_counter(cnt, album_dir / "summary.json")