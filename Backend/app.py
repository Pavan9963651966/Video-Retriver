from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from search import search_videos  # Import search function

app = Flask(__name__)

# Set video storage directory (change this if videos are stored elsewhere)
VIDEO_DIR = "data/videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Video Retriever API!"})

@app.route("/upload", methods=["POST"])
def upload_video():
    """Upload video and save it in the storage folder."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    file_path = os.path.join(VIDEO_DIR, filename)
    file.save(file_path)

    return jsonify({"message": "Video uploaded successfully", "filename": filename})

@app.route("/search", methods=["GET"])
def search():
    """Search videos based on user query."""
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    results = search_videos(query)
    return jsonify(results)

@app.route("/videos/<filename>", methods=["GET"])
def get_video(filename):
    """Return video file from storage"""
    return send_from_directory(VIDEO_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
