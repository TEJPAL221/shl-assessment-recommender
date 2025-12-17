from backend.app.retrieval.semantic_search import SemanticSearchEngine

engine = SemanticSearchEngine()

query = "Java developer with strong problem solving and numerical skills"
results = engine.search(query, top_k=5)

for r in results:
    print("-", r["assessment_name"])
