import whisper
import json
import os
from sentence_transformers import SentenceTransformer
import numpy as np

VIDEO_DIR = "data/videos"
EMBEDDING_DIR = "data/embeddings"
os.makedirs(EMBEDDING_DIR, exist_ok=True)

model = whisper.load_model("base")
embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

def transcribe_and_save(video_path, video_name):
    """Extract text from video and save embeddings"""
    result = model.transcribe(video_path)
    text = result["text"]

    # Generate text embeddings
    embedding = embedding_model.encode(text).tolist()

    # Save embeddings as JSON
    embedding_data = {
        "video_name": video_name,
        "embedding": embedding,
        "transcription": text
    }
    with open(os.path.join(EMBEDDING_DIR, f"{video_name}.json"), "w") as f:
        json.dump(embedding_data, f)

    return text

if __name__ == "__main__":
    # Process all videos
    for video in os.listdir(VIDEO_DIR):
        if video.endswith(".mp4") or video.endswith(".avi"):
            transcribe_and_save(os.path.join(VIDEO_DIR, video), video)
