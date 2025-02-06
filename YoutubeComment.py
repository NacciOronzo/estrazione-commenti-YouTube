from youtube_comment_downloader import YoutubeCommentDownloader
import streamlit as st

def get_youtube_comments(video_url, max_comments=100):
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments(video_url, max_count=max_comments)
    return [comment['text'] for comment in comments]

st.title("Estrattore Commenti YouTube")

video_url = st.text_input("Inserisci l'URL del video YouTube")

if st.button("Estrai Commenti"):
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
