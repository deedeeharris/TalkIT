import streamlit as st
import os
import docx
from gtts import gTTS
from tqdm import tqdm
import time

def read_docx(file_path):
    document = docx.Document(file_path)
    text = []
    for paragraph in document.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

def generate_mp3(text, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    tts = gTTS(text=text, lang='en')

    # Estimate the speech length based on the number of characters
    speech_length = len(text) / 16  # Assuming 16 characters per second

    # Create a progress bar with the total length of the speech
    progress_bar = tqdm(total=speech_length, unit='sec', desc='Generating MP3', ncols=80)

    # Save the speech as an MP3 file
    tts.save(file_path)

    # Update the progress bar every second until it reaches the estimated length
    current_duration = 0
    while current_duration < speech_length:
        time.sleep(1)
        current_duration += 1
        progress_bar.update(1)

    # Close the progress bar
    progress_bar.close()

# Streamlit app
st.title("Text-to-Speech Converter")

# File upload
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

    st.write("## Text Content")
    st.write(text)

    if st.button("Generate MP3"):
        with st.spinner("Generating MP3..."):
            mp3_file_path = "generated_audio.mp3"  # Change the file name as desired
            generate_mp3(text, mp3_file_path)
            st.success("MP3 file generated successfully.")

            # Download the MP3 file
            st.download_button("Download MP3", mp3_file_path, "mp3")
