import streamlit as st
import os
import docx
from gtts import gTTS
from tqdm import tqdm
import time
import tempfile
from pydub import AudioSegment
import base64

def read_docx(file_path):
    document = docx.Document(file_path)
    text = []
    for paragraph in document.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

def generate_mp3(text, file_path):
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, "temp.mp3")

    tts = gTTS(text=text, lang='en')

    # Save the speech as a temporary MP3 file
    tts.save(temp_file_path)

    # Move the temporary MP3 file to the desired location
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    os.rename(temp_file_path, file_path)

# Streamlit app
st.title("Text-to-Speech Converter")

# Text input or file upload
option = st.radio("Select Input Option", ("Upload File", "Enter Text"))

if option == "Upload File":
    uploaded_file = st.file_uploader("Upload a DOCX or TXT file", type=["docx", "txt"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]

        if file_extension.lower() == "docx":
            text = read_docx(uploaded_file)
        elif file_extension.lower() == "txt":
            text = uploaded_file.read().decode("utf-8")
        else:
            st.error("Invalid file format. Please upload a DOCX or TXT file.")
            st.stop()
else:
    text = st.text_area("Enter the text")

if text:
    st.write("## Text Content")
    st.write(text)

    if st.button("Generate MP3"):
        with st.spinner("Generating MP3..."):
            mp3_file_path = os.path.join(tempfile.gettempdir(), "generated_audio.mp3")
            generate_mp3(text, mp3_file_path)
            st.success("MP3 file generated successfully.")

            # Play the MP3 file
            audio = AudioSegment.from_file(mp3_file_path, format="mp3")
            st.audio(audio)

            # Download the MP3 file
            with open(mp3_file_path, "rb") as file:
                st.download_button("Download MP3", file.read(), file_name="generated_audio.mp3", mime="audio/mpeg")
