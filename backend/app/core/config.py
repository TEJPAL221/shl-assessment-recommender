# backend/app/core/config.py

APP_NAME = "SHL Assessment Recommender"
TOP_K_RECOMMENDATIONS = 10

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

FAISS_INDEX_PATH = "data/embeddings/index.faiss"
METADATA_PATH = "data/embeddings/metadata.pkl"
