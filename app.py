import streamlit as st
import pdfplumber
import pyttsx3
import base64

# Add this line to modify the HTML head section
st.set_page_config(page_title="TalkIt - PDF to mp3!", page_icon="favicon.ico")

st.title("TalkIt - PDF to mp3!")
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

    # Initialize pyttsx3 TTS engine
    engine = pyttsx3.init()

    # Save the text to an audio file
    audio_file = "audio_book.mp3"
    engine.save_to_file(all_text, audio_file)
    engine.runAndWait()

    # Download audio file
    with open(audio_file, 'rb') as audio_file:
        audio_bytes = audio_file.read()
        b64 = base64.b64encode(audio_bytes).decode()
        href = f'<a href="data:audio/mp3;base64,{b64}" download="audio_book.mp3">Download Your Audio File</a>'
        st.markdown(href, unsafe_allow_html=True)

    audio_file = open(audio_file, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')
