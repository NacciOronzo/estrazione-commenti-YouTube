from youtube_comment_downloader import YoutubeCommentDownloader
import streamlit as st
import re
import pandas as pd

def extract_video_id(url):
    """Estrae l'ID del video da un URL YouTube"""
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None

def get_youtube_comments(video_url, max_comments=100):
    video_id = extract_video_id(video_url)
    if not video_id:
        st.error("❌ URL non valido. Inserisci un link YouTube corretto.")
        return []

    downloader = YoutubeCommentDownloader()
    comments = list(downloader.get_comments(video_id))[:max_comments]
    return [comment['text'] for comment in comments]

st.title("Estrattore Commenti YouTube")

video_url = st.text_input("Inserisci l'URL del video YouTube")

col1, col2 = st.columns(2)
with col1:
    extract_button = st.button("Estrai Commenti")
with col2:
    download_button = st.button("Scarica Commenti")

comments = []
if extract_button:
    if video_url:
        st.write("🚀 Recupero dei commenti...")
        comments = get_youtube_comments(video_url, max_comments=100)
        if comments:
            for i, comment in enumerate(comments, 1):
                st.write(f"{i}. {comment}")
        else:
            st.write("❌ Nessun commento trovato.")
    else:
        st.error("Inserisci un URL valido!")

if download_button and comments:
    df = pd.DataFrame(comments, columns=["Commenti"])
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Scarica CSV", data=csv, file_name="commenti_youtube.csv", mime="text/csv")
