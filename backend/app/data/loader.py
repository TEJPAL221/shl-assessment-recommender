import json
import os

# Resolve project root dynamically
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)

CLEAN_PATH = os.path.join(
    BASE_DIR, "data", "processed", "shl_catalog_clean.json"
)


def load_catalog():
    if not os.path.exists(CLEAN_PATH):
        raise FileNotFoundError(f"Clean catalog not found at {CLEAN_PATH}")

    with open(CLEAN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Catalog data is not a list")

    return data
