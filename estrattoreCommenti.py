import time
import streamlit as st
from playwright.sync_api import sync_playwright

def get_youtube_comments(video_url, max_comments=100):
    comments = []
    with sync_playwright() as p:
        st.write("▶ Avvio Playwright...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        st.write("🔄 Caricamento della pagina...")
        page.goto(video_url, wait_until="domcontentloaded")
        time.sleep(5)
        
        # Gestione della modale dei cookie
        try:
            reject_button = page.locator('button:has-text("Reject all")')
            if reject_button.is_visible():
                reject_button.click()
                st.write("🍪 Modale chiusa con successo!")
                time.sleep(2)
        except:
            st.write("✅ Nessuna modale trovata.")
        
        last_count = 0
        retries = 0
        time.sleep(5)
        st.write("🔽 Inizio scorrimento per caricare i commenti...")

        while len(comments) < max_comments and retries < 7:
            page.mouse.wheel(0, 2000)
            st.write("📜 Scrolling...")
            time.sleep(2)
            comment_elements = page.locator("#content-text").all()
            comments = [comment.inner_text() for comment in comment_elements]

            if len(comments) == last_count:
                retries += 1
                st.write(f"⚠️ Nessun nuovo commento trovato. Tentativo {retries}/7...")
            else:
                retries = 0
                st.write(f"📩 Commenti estratti finora: {len(comments)}")
            
            last_count = len(comments)

        browser.close()
        st.write("✅ Estrazione completata.")
    return comments[:max_comments]

st.title("Estrattore Commenti YouTube")

video_url = st.text_input("Inserisci l'URL del video YouTube")

if st.button("Estrai Commenti"):
    if video_url:
        st.write("🚀 Avvio dell'estrazione...")
        comments = get_youtube_comments(video_url, max_comments=100)
        
        if comments:
            for i, comment in enumerate(comments, 1):
                st.write(f"{i}. {comment}")
        else:
            st.write("❌ Nessun commento trovato.")
    else:
        st.error("Inserisci un URL valido!")
