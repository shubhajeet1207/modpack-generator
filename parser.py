import json
from typing import List, Tuple, Dict


def load_mods() -> Tuple[str, List[str]]:
    with open("mods.txt") as f:
        version = f.readline()[2:]
        mods = [x.strip() for x in f.readlines() if x.strip()]

    return version, mods


def load_config() -> Dict[str, str]:
    with open("config.json") as f:
        return json.load(f)