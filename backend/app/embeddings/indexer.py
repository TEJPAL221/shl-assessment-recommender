import faiss
import pickle
import os

from backend.app.data.loader import load_catalog
from backend.app.embeddings.embedder import SHLEmbedder


# Resolve project root dynamically
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)

# Ensure embeddings directory exists
EMBEDDINGS_DIR = os.path.join(BASE_DIR, "data", "embeddings")
INDEX_PATH = os.path.join(EMBEDDINGS_DIR, "index.faiss")
META_PATH = os.path.join(EMBEDDINGS_DIR, "metadata.pkl")


def build_index():
    print("[INFO] Loading cleaned SHL catalog...")
    catalog = load_catalog()
    print(f"[INFO] Catalog size: {len(catalog)}")

    embedder = SHLEmbedder()

    print("[INFO] Generating embeddings...")
    embeddings = embedder.encode_catalog(catalog)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    print(f"[INFO] FAISS index built with {index.ntotal} vectors")

    # ✅ Create directory if missing
    os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump(catalog, f)

    print("[SUCCESS] FAISS index and metadata saved")


if __name__ == "__main__":
    build_index()
