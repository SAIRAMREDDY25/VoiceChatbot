import streamlit as st
import os
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

# Float feature initialization
float_init()

# Initialize session state
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I assist you today?"}
        ]
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "audio_playback" not in st.session_state:
        st.session_state.audio_playback = None
    if "new_question" not in st.session_state:
        st.session_state.new_question = False
    if "processed" not in st.session_state:
        st.session_state.processed = False  # Track if input has been processed

initialize_session_state()

# Function to handle user input submission
def submit_text_input():
    if st.session_state.user_input:
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_input})
        st.session_state.new_question = True  # Flag that a new question is submitted
        st.session_state.user_input = ""  # Clear the input after submission
        st.session_state.processed = True  # Mark the input as processed

# Handle audio input (for microphone recording)
def handle_audio_input(audio_bytes):
    if audio_bytes and not st.session_state.processed:  # Only process if no input was previously processed
        with st.spinner("Transcribing..."):
            webm_file_path = "temp_audio.mp3"
            with open(webm_file_path, "wb") as f:
                f.write(audio_bytes)

            transcript = speech_to_text(webm_file_path)
            if transcript:
                st.session_state.messages.append({"role": "user", "content": transcript})
                st.session_state.new_question = True  # Flag that a new question is submitted
                st.session_state.processed = True  # Mark the input as processed
                os.remove(webm_file_path)

# Generate assistant response
def generate_assistant_response():
    if st.session_state.new_question and st.session_state.processed:
        with st.chat_message("assistant"):
            with st.spinner("Thinking... 🤔"):
                final_response = get_answer(st.session_state.messages)
            with st.spinner("Generating audio response..."):
                audio_file = text_to_speech(final_response)
                
                # Store the audio playback in session state for play/pause
                st.session_state.audio_playback = audio_file
                
                # Append response to the messages
                st.session_state.messages.append({"role": "assistant", "content": final_response})
                
                # Reset new_question and processed flag after generating the response
                st.session_state.new_question = False
                st.session_state.processed = False

# Title of the app
st.title("Conversational Chatbot 🤖")

# Create footer container for audio input and text input
footer_container = st.container()

with footer_container:
    # Audio input
    audio_bytes = audio_recorder()
    
    # Text input (at the bottom), using on_change to submit automatically
    st.text_input("Type your message here...", key="user_input", on_change=submit_text_input)

# Process user inputs before rendering messages
handle_audio_input(audio_bytes)

# Only generate a response if a new question has been submitted and processed
generate_assistant_response()

# Display conversation above input
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Audio controls for the last response
if st.session_state.audio_playback:
    st.audio(st.session_state.audio_playback, format="audio/mp3")

# Float footer to bottom
footer_container.float("bottom: 0rem;")
