import json
from pathlib import Path
from classes import Scenes


def gen_json_file(scenes: Scenes, out_file: Path, indent: int = 4) -> None:
    with open(out_file, "w") as f:
        json.dump(scenes, f, indent=indent)