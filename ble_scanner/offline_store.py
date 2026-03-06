import json
import os
from config import OFFLINE_FILE


def save_offline(data):

    if os.path.exists(OFFLINE_FILE):

        with open(OFFLINE_FILE, "r") as f:
            existing = json.load(f)

    else:

        existing = []

    existing.append(data)

    with open(OFFLINE_FILE, "w") as f:
        json.dump(existing, f, indent=2)