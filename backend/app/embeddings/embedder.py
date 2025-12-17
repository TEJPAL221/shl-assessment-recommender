from sentence_transformers import SentenceTransformer
import numpy as np


class SHLEmbedder:
    def __init__(self):
        # Stable, proven model for semantic retrieval
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def _build_embedding_text(self, assessment: dict) -> str:
        """
        Build a rich, structured text representation for embedding.
        This is the key Phase 4A improvement.
        """

        name = assessment.get("name", "")
        description = assessment.get("description", "")
        test_types = assessment.get("test_type", [])

        # Normalize test type
        if isinstance(test_types, list):
            test_type_text = ", ".join(test_types)
        else:
            test_type_text = str(test_types)

        # Infer role / skill hints from name (lightweight, deterministic)
        role_hints = []
        name_lower = name.lower()

        if any(k in name_lower for k in ["java", "python", "programming", "developer", "coding"]):
            role_hints.append("software developer, programmer, engineer")

        if any(k in name_lower for k in ["manager", "lead", "supervisor"]):
            role_hints.append("manager, team lead, leadership role")

        if any(k in name_lower for k in ["sales", "account", "customer"]):
            role_hints.append("sales, customer service, client-facing roles")

        if any(k in name_lower for k in ["personality", "behavior", "situational", "opq"]):
            role_hints.append("behavioral assessment, personality traits, soft skills")

        role_hint_text = "; ".join(role_hints) if role_hints else "general professional roles"

        # Final enriched embedding text
        embedding_text = f"""
        Assessment Name: {name}

        Description:
        {description}

        Assessment Type:
        {test_type_text}

        Suitable for roles involving:
        {role_hint_text}

        This assessment helps evaluate job-related skills, competencies,
        cognitive abilities, and behavioral traits relevant to hiring decisions.
        """

        return embedding_text.strip()

    def encode_catalog(self, catalog: list) -> np.ndarray:
        """
        Encode full SHL catalog into dense vectors.
        """
        texts = [self._build_embedding_text(item) for item in catalog]
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            normalize_embeddings=True
        )
        return embeddings
