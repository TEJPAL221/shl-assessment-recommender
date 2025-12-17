import csv
import os

from backend.app.retrieval.semantic_search import SemanticSearchEngine


# --------------------------------------------------
# BASE PATHS (LOCKED TO PROJECT STRUCTURE)
# --------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)

TEST_PATH = os.path.join(
    BASE_DIR, "data", "test", "unlabeled_test.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR, "outputs", "test_predictions.csv"
)

TOP_K = 10


# --------------------------------------------------
# LOAD TEST QUERIES
# --------------------------------------------------

def load_test_queries():
    queries = []

    # cp1252 handles Excel-exported CSV safely
    with open(TEST_PATH, newline="", encoding="cp1252") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = row.get("Query", "").strip()
            if query:
                queries.append(query)

    return queries


# --------------------------------------------------
# GENERATE TEST PREDICTIONS
# --------------------------------------------------

def generate_predictions():
    print("[INFO] Initializing semantic search engine...")
    engine = SemanticSearchEngine()

    print("[INFO] Loading test queries...")
    queries = load_test_queries()
    print(f"[INFO] Loaded {len(queries)} test queries")

    rows = []

    for idx, query in enumerate(queries, start=1):
        print(f"[{idx}/{len(queries)}] Generating recommendations...")
        results = engine.search(query, top_k=TOP_K)

        for item in results:
            rows.append({
                "Query": query,
                "Assessment_url": item["assessment_url"]
            })

    # Ensure outputs directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    print("[INFO] Writing predictions CSV...")
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Query", "Assessment_url"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print("[SUCCESS] Test predictions generated successfully")
    print(f"[SUCCESS] File saved at: {OUTPUT_PATH}")


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    generate_predictions()
