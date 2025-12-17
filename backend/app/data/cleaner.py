import json

RAW_PATH = "../../../data/raw/shl_catalog_raw.json"
CLEAN_PATH = "../../../data/processed/shl_catalog_clean.json"


def clean():
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    cleaned = []
    for item in raw_data:
        if not item.get("assessment_name"):
            continue
        if not item.get("assessment_url"):
            continue
        if "job" in item["assessment_name"].lower():
            continue
        cleaned.append(item)

    print(f"[INFO] Cleaned dataset size: {len(cleaned)}")

    if len(cleaned) < 377:
        raise RuntimeError(
            f"❌ Requirement failed: only {len(cleaned)} assessments found (minimum 377 required)"
        )

    with open(CLEAN_PATH, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print("[SUCCESS] Clean dataset saved successfully")


if __name__ == "__main__":
    clean()
