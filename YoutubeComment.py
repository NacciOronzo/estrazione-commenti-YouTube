from youtube_comment_downloader import YoutubeCommentDownloader
import streamlit as st
import time

def get_youtube_comments(video_url, max_comments=100):
    downloader = YoutubeCommentDownloader()
    st.write("▶ Avvio del downloader...")
    # Passa direttamente l'URL completo
    comments = downloader.get_comments(video_url, max_count=max_comments)
    st.write("📩 Commenti recuperati:", len(comments))
    return [comment['text'] for comment in comments]

st.title("Estrattore Commenti YouTube")

video_url = st.text_input("Inserisci l'URL del video YouTube")

if st.button("Estrai Commenti"):
    if video_url:
        with st.spinner("🚀 Recupero dei commenti in corso..."):
            try:
                comments = get_youtube_comments(video_url, max_comments=100)
            except Exception as e:
                st.error(f"Errore durante il recupero dei commenti: {e}")
                comments = []
        if comments:
            st.write("✅ Estrazione completata!")
            for i, comment in enumerate(comments, 1):
                st.write(f"{i}. {comment}")
        else:
            st.write("❌ Nessun commento trovato.")
    else:
        st.error("Inserisci un URL valido!")
