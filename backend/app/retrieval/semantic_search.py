import faiss
import pickle
import numpy as np
import os

from backend.app.embeddings.embedder import SHLEmbedder


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)

INDEX_PATH = os.path.join(BASE_DIR, "data", "embeddings", "index.faiss")
META_PATH = os.path.join(BASE_DIR, "data", "embeddings", "metadata.pkl")


class SemanticSearchEngine:
    def __init__(self):
        self.embedder = SHLEmbedder()

        self.index = faiss.read_index(INDEX_PATH)

        with open(META_PATH, "rb") as f:
            self.catalog = pickle.load(f)

    # -------------------------
    # Query intent detection
    # -------------------------
    def _detect_intent(self, query: str) -> str:
        q = query.lower()

        technical_keywords = [
            "java", "python", "developer", "coding", "programming",
            "technical", "engineer", "software", "data"
        ]

        behavioral_keywords = [
            "collaborate", "communication", "team", "leadership",
            "interpersonal", "behavior", "soft skill", "personality"
        ]

        has_tech = any(k in q for k in technical_keywords)
        has_behav = any(k in q for k in behavioral_keywords)

        if has_tech and has_behav:
            return "mixed"
        elif has_behav:
            return "behavioral"
        else:
            return "technical"

    # -------------------------
    # Reranking logic
    # -------------------------
    def _rerank(self, candidates: list, intent: str, top_k: int) -> list:
        """
        Enforce K / P balance for mixed queries.
        """
        if intent != "mixed":
            return candidates[:top_k]

        k_tests = []
        p_tests = []
        others = []

        for item in candidates:
            test_types = item.get("test_type", [])

            if "K" in test_types:
                k_tests.append(item)
            elif "P" in test_types:
                p_tests.append(item)
            else:
                others.append(item)

        final = []

        # Enforce at least one K and one P if available
        if k_tests:
            final.append(k_tests.pop(0))
        if p_tests:
            final.append(p_tests.pop(0))

        # Fill remaining slots by original relevance order
        remaining = k_tests + p_tests + others

        for item in remaining:
            if len(final) >= top_k:
                break
            final.append(item)

        return final[:top_k]

    # -------------------------
    # Public search API
    # -------------------------
    def search(self, query: str, top_k: int = 10):
        # Embed query
        query_vec = self.embedder.model.encode(
            [query],
            normalize_embeddings=True
        ).astype("float32")

        # Retrieve top-20 for reranking headroom
        scores, indices = self.index.search(query_vec, 40)

        candidates = []
        for idx in indices[0]:
            item = self.catalog[idx]
            candidates.append({
                "assessment_name": item["assessment_name"],
                "assessment_url": item["assessment_url"],
                "description": item["description"],
                "test_type": item.get("test_type", []),
                "duration": item.get("duration", ""),
                "remote_testing": item.get("remote_testing", ""),
                "adaptive_support": item.get("adaptive_support", "")
            })

        intent = self._detect_intent(query)

        return self._rerank(candidates, intent, top_k)
