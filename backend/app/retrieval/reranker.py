from typing import List, Dict


class AssessmentReranker:
    def __init__(self, top_k: int = 5):
        self.top_k = top_k

    def rerank(self, candidates: List[Dict]) -> List[Dict]:
        """
        Balance technical (K) and behavioral (P) assessments.
        """
        technical = []
        behavioral = []
        others = []

        for item in candidates:
            types = item.get("test_type", [])
            if "K" in types:
                technical.append(item)
            elif "P" in types:
                behavioral.append(item)
            else:
                others.append(item)

        results = []

        # Prefer balance if possible
        if technical and behavioral:
            results.extend(technical[:3])
            results.extend(behavioral[:2])
        else:
            results.extend(technical[:self.top_k])
            results.extend(behavioral[:self.top_k])

        # Fill remaining slots if needed
        if len(results) < self.top_k:
            remaining = [
                x for x in candidates
                if x not in results
            ]
            results.extend(remaining[: self.top_k - len(results)])

        return results[:self.top_k]
