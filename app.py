import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import io
from gtts import gTTS
import base64
# Function to convert audio file to WAV format
# def convert_to_wav(audio_file):
#     audio = AudioSegment.from_file(io.BytesIO(audio_file.read()))
#     audio = audio.set_channels(1)  # Ensure mono audio
#     audio = audio.set_frame_rate(16000)  # Ensure 16kHz sample rate
#     wav_data = audio.raw_data
#     return wav_data

# Function to convert speech to text
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

# Function to convert text to speech
def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language)
    with io.BytesIO() as f:
        tts.write_to_fp(f)
        f.seek(0)
        audio_bytes = f.read()
    return audio_bytes

# Function to read text from a file
def read_text_from_file(uploaded_file):
    text = uploaded_file.getvalue().decode("utf-8")
    return text

# Streamlit app

# Streamlit app
def main():
    st.title("Text to Speech & Speech to Text")

    option = st.selectbox("Select an option:", ("Text to Speech", "Speech to Text"))

    if option == "Text to Speech":
        st.header("Text to Speech")
        text_option = st.radio("Select input option:", ("Enter text", "Upload text file"))

        if text_option == "Enter text":
            text = st.text_area("Enter text")
        elif text_option == "Upload text file":
            uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
            if uploaded_file is not None:
                text = read_text_from_file(uploaded_file)

        language = st.selectbox("Select language:", ("English", "French", "Spanish"))  # Add more languages as needed
        language_code = {'English': 'en', 'French': 'fr', 'Spanish': 'es'}
        if st.button("Convert"):
            audio_bytes = text_to_speech(text, language=language_code[language])
            st.audio(audio_bytes, format='audio/mp3')

            # Download button for audio file
            st.markdown(get_binary_file_downloader_html(audio_bytes, 'audio.mp3', 'Download Audio'), unsafe_allow_html=True)

    elif option == "Speech to Text":
        st.header("Speech to Text")
        uploaded_file = st.file_uploader("Upload an audio file", type=["wav"])

        if uploaded_file is not None:
            if st.button("Convert"):
                try:
                    text = speech_to_text(uploaded_file)
                    st.write("Transcribed Text:")
                    st.write(text)
                    st.markdown(get_binary_file_downloader_html(text.encode(), 'Transcribed_Text.txt', 'Download Transcribed Text'), unsafe_allow_html=True)
                except sr.UnknownValueError:
                    st.error("Error: Could not understand audio")
                except sr.RequestError as e:
                    st.error(f"Error occurred: {e}")

def get_binary_file_downloader_html(bin_file, file_label='File', button_label='Download'):
    """
    Generates a link to download the given binary file.
    """
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">{button_label}</a>'
    return href

if __name__ == "__main__":
    main()