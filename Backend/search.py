from sentence_transformers import SentenceTransformer
import numpy as np
import os
import json

# Load embedding model
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Directory for video text embeddings
EMBEDDING_DIR = "data/embeddings"
os.makedirs(EMBEDDING_DIR, exist_ok=True)

def load_embeddings():
    """Load all stored video embeddings"""
    embeddings = {}
    for file in os.listdir(EMBEDDING_DIR):
        if file.endswith(".json"):
            with open(os.path.join(EMBEDDING_DIR, file), "r") as f:
                data = json.load(f)
                embeddings[data["video_name"]] = np.array(data["embedding"])
    return embeddings

def search_videos(query):
    """Search videos using text similarity"""
    query_embedding = model.encode(query)
    embeddings = load_embeddings()

    results = []
    for video_name, video_embedding in embeddings.items():
        similarity = np.dot(query_embedding, video_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(video_embedding))
        results.append((video_name, similarity))
    
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"video": r[0], "score": r[1]} for r in results[:5]]  # Return top 5 matches
