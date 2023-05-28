import streamlit as st
import pdfplumber
from gtts import gTTS

st.title("TalkIt - PDF to mp3!")

# App created by Yedidya Harris
st.markdown("#### by [Yedidya Harris](https://www.linkedin.com/in/yedidya-harris)")

st.markdown("## Please upload your PDF")
book = st.file_uploader("")

if book is not None:
    # Progress bar initialization
    progress_bar = st.progress(0)

    with pdfplumber.open(book) as pdf:
        all_text = ""
        total_pages = len(pdf.pages)
        
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            all_text += text + "\n"

            # Update progress bar
            progress = (i + 1) / total_pages
            progress_bar.progress(progress)

    tts = gTTS(all_text)
    tts.save('audio_book.mp3')

    # Download audio file
    st.download_button(
        label="Download Your Audio File",
        data='audio_book.mp3',
        file_name='audio_book.mp3',
        mime='audio/mp3'
    )

    audio_file = open('audio_book.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')
