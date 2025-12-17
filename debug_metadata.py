import pickle

with open("data/embeddings/metadata.pkl", "rb") as f:
    catalog = pickle.load(f)

print("Total items:", len(catalog))
print("Keys in first item:", catalog[0].keys())
print("Sample item:", catalog[0])
