from youtube_comment_downloader import YoutubeCommentDownloader
import streamlit as st
import re
import time

def extract_video_id(url):
    """Estrae l'ID del video da un URL YouTube."""
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None

def get_youtube_comments(video_url, max_comments=100):
    video_id = extract_video_id(video_url)
    if not video_id:
        st.error("❌ URL non valido. Inserisci un link YouTube corretto.")
        return []
    
    try:
        downloader = YoutubeCommentDownloader()
        st.write("▶ Avvio del downloader per il video con ID:", video_id)
        # Rimuoviamo l'argomento 'max_count' dalla chiamata
        comments = downloader.get_comments(video_id)
        st.write("📩 Commenti recuperati:", len(comments))
        # Limitiamo il numero di commenti restituendo solo i primi max_comments
        return [comment['text'] for comment in comments][:max_comments]
    except Exception as e:
        st.error(f"Errore nel recupero dei commenti: {e}")
        return []

st.title("Estrattore Commenti YouTube")

video_url = st.text_input("Inserisci l'URL del video YouTube")

if st.button("Estrai Commenti"):
    if video_url:
        st.write("🚀 Recupero dei commenti...")
        comments = get_youtube_comments(video_url, max_comments=100)
        if comments:
            st.write("✅ Estrazione completata!")
            for i, comment in enumerate(comments, 1):
                st.write(f"{i}. {comment}")
        else:
            st.write("❌ Nessun commento trovato.")
    else:
        st.error("Inserisci un URL valido!")
