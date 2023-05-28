import streamlit as st
import pdfplumber
from gtts import gTTS

st.title("Convert all your E-books to Audio Books just like that!")
book = st.file_uploader("Please upload your PDF")

if book is not None:
    with pdfplumber.open(book) as pdf:
        all_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            all_text += text + "\n"
    
    tts = gTTS(all_text)
    tts.save('audio_book.mp3')

    audio_file = open('audio_book.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')
