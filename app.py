import streamlit as st
import pdfplumber
import pyttsx3

# Add this line to modify the HTML head section
st.set_page_config(page_title="TalkIt - PDF to Text!", page_icon="favicon.ico")

st.title("TalkIt - PDF to Text!")
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

    # Initialize pyttsx3 TTS engine with the "dummy" driver
    engine = pyttsx3.init(driverName='dummy')

    # Display the text on the screen
    st.text_area("Extracted Text", value=all_text, height=400)

