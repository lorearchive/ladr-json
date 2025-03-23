import os
import re
import json

# Constants
VOLUME_DIRS = [f"Volume{i}" for i in range(1, 6)]
EPISODE_PATTERN = re.compile(r"Episode(\d+)-s([12])\.json")

def process_directory(path):
    meta = {}

    # Find matching episode files
    episodes = {}
    for filename in os.listdir(path):
        match = EPISODE_PATTERN.match(filename)
        if match:
            episode_num = match.group(1)
            sector = match.group(2)
            if episode_num not in episodes:
                episodes[episode_num] = set()
            episodes[episode_num].add(sector)

    # Fill meta data
    for ep_num in sorted(episodes.keys(), key=lambda x: int(x)):
        meta[ep_num] = {
            "Sectors": 2 if '2' in episodes[ep_num] else 1
        }

    # Write to .meta.json if not exists
    meta_path = os.path.join(path, ".meta.json")
    if not os.path.exists(meta_path):
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        print(f"Created: {meta_path}")
    else:
        print(f"Skipped (exists): {meta_path}")

def recursive_check(path):
    # Check current dir
    process_directory(path)
    # Check subdirs
    for root, dirs, _ in os.walk(path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            process_directory(dir_path)

def main():
    current_dir = os.getcwd()
    entries = os.listdir(current_dir)

    # Check required volume dirs
    for vol in VOLUME_DIRS:
        if vol in entries:
            volume_path = os.path.join(current_dir, vol)
            recursive_check(volume_path)

if __name__ == "__main__":
    main()

