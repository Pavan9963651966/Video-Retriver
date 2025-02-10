import streamlit as st
import requests

st.title("🎥 Video Retriever")

# Upload Video
st.subheader("Upload a Video")
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post("http://127.0.0.1:5000/upload", files=files)
    if response.status_code == 200:
        st.success("Video uploaded successfully!")

# Search Videos
st.subheader("Search for Relevant Videos")
query = st.text_input("Enter your query")

if query:
    response = requests.get(f"http://127.0.0.1:5000/search?query={query}")
    if response.status_code == 200:
        videos = response.json()
        if videos:
            st.write("Top Matches:")
            for video in videos:
                st.video(f"http://127.0.0.1:5000/videos/{video['video']}")
                st.write(f"**{video['video']}** (Similarity: {video['score']:.2f})")
        else:
            st.warning("No relevant videos found.")
