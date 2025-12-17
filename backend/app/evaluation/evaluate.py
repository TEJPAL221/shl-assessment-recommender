import csv
import os
import pickle
from collections import defaultdict
from statistics import mean
from urllib.parse import urlparse

from backend.app.retrieval.semantic_search import SemanticSearchEngine
from backend.app.evaluation.recall import recall_at_k


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)

TRAIN_PATH = os.path.join(BASE_DIR, "data", "train", "labeled_train.csv")
META_PATH = os.path.join(BASE_DIR, "data", "embeddings", "metadata.pkl")


def normalize_shl_url(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url.strip())
    path = parsed.path.rstrip("/")
    return path.split("/")[-1].lower()


def load_valid_catalog_slugs():
    with open(META_PATH, "rb") as f:
        catalog = pickle.load(f)

    # ✅ FIX: use assessment_url
    return {
        normalize_shl_url(item.get("assessment_url", ""))
        for item in catalog
        if item.get("assessment_url")
    }


def load_and_group_train_data(valid_slugs):
    grouped = defaultdict(set)

    with open(TRAIN_PATH, newline="", encoding="cp1252") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = row["Query"].strip()
            slug = normalize_shl_url(row["Assessment_url"])

            # Keep only labels that exist in catalog
            if query and slug in valid_slugs:
                grouped[query].add(slug)

    return grouped


def evaluate_recall_at_10():
    engine = SemanticSearchEngine()

    valid_slugs = load_valid_catalog_slugs()
    grouped_data = load_and_group_train_data(valid_slugs)

    print(f"[INFO] Evaluating {len(grouped_data)} valid training queries\n")

    recalls = []

    for i, (query, relevant_slugs) in enumerate(grouped_data.items(), start=1):

        results = engine.search(query, top_k=10)
        retrieved_slugs = [
            normalize_shl_url(r["assessment_url"])
            for r in results
        ]

        r10 = recall_at_k(relevant_slugs, retrieved_slugs, k=10)
        recalls.append(r10)

        print(f"[{i}] Recall@10 = {r10:.2f}")

    mean_recall = mean(recalls) if recalls else 0.0

    print("\n==============================")
    print(f"Mean Recall@10: {mean_recall:.3f}")
    print("==============================")

    return mean_recall


if __name__ == "__main__":
    evaluate_recall_at_10()
