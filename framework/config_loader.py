import json
from pathlib import Path

def load_config(config_path='tests/config.json'):
    # First try the provided path
    path = Path(config_path)

    # If not found, try relative to the project root
    if not path.is_file():
        project_root = Path(__file__).parent.parent
        path = project_root / config_path

    if not path.is_file():
        raise FileNotFoundError(f"Config file not found at {path.resolve()}")

    with open(path, 'r') as f:
        config = json.load(f)
    return config