# **Voice-Based Chatbot with OpenAI**

This project demonstrates a **voice-based conversational chatbot** built using **Streamlit**, **OpenAI's GPT-3.5-turbo**, **Whisper** (for speech-to-text), and **Text-to-Speech (TTS)** models. The chatbot allows users to interact with the AI assistant via both **text** and **speech** in real-time.

## **Features**

- **Text & Voice Input**: Seamless interaction through either text or voice.
- **Speech-to-Text**: Converts voice input to text using OpenAI's Whisper model.
- **Text-to-Speech**: Generates audio responses using OpenAI's TTS model.
- **Real-time Conversations**: Responses are generated and played back as audio or text in real time.
- **Persistent Context**: Remembers conversation history for continuous interaction.
- **Interactive UI**: Simple, clean, and user-friendly interface built with Streamlit.

---

## **Tech Stack**

- **Python 3.10+**
- **Streamlit**: Web app framework for building the UI.
- **OpenAI API**: GPT-3.5-turbo for conversation, Whisper for speech-to-text, and TTS for speech generation.
- **Audio Recorder Streamlit**: For recording audio input.
- **dotenv**: For managing environment variables (e.g., OpenAI API key).

---

## **Prerequisites**

1. **Python**: Ensure Python 3.7 or later is installed on your system.
   
2. **OpenAI API Key**: You need an OpenAI API key to access GPT models, Whisper, and Text-to-Speech. You can get one from [OpenAI](https://platform.openai.com/account/api-keys).

3. **Streamlit Setup**: You should have Streamlit installed to run the app locally.

---

## **Installation**

1. Clone this repository to your local machine:

   Using OpenAI
    ```bash
    git clone https://github.com/SAIRAMREDDY25/VoiceChatbot.git
    cd VoiceChatbot
    ```
   Using AWS-Services
    ```bash
    git clone https://github.com/SAIRAMREDDY25/VoiceChatbot.git
    cd VoiceChatbot/UsingAWS-Services
    ```
    

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

---

## **Configuration**

1. Create a `.env` file in the root of the project directory and add your OpenAI API key as follows:

    ```env
    OPENAI_API_KEY=your-openai-api-key-here
    ```

---

## **Running the Application**

Once the setup is complete, you can run the Streamlit app locally:

```bash
streamlit run app.py
```

This will start the app and open it in your default web browser, where you can interact with the chatbot.

---

## **How It Works**

### **1. Text Input**
Users can type their queries into a text box, and the chatbot will process the input and provide a response using the **GPT-3.5-turbo** model. The response is then spoken back to the user using OpenAI's **Text-to-Speech** model.

### **2. Voice Input**
Users can record their voice using the inbuilt microphone recorder, and the recorded audio is then transcribed into text using **OpenAI's Whisper** model. This text is then processed by the GPT model to generate a reply, which is converted to speech and played back.

### **3. Audio Playback**
The chatbot's responses are automatically converted to audio and played back to the user using the **Text-to-Speech** functionality.

### **4. Continuous Interaction**
The chatbot maintains context for the ongoing conversation, providing relevant and coherent responses based on the conversation history.

---

## **File Structure**

```plaintext
.
├── app.py                  # Main Streamlit application file
├── utils.py                # Helper functions for OpenAI API integration (Speech-to-Text, Text-to-Speech, etc.)
├── .env                    # File for storing the OpenAI API key securely
├── requirements.txt        # Required Python libraries for the project
├── README.md               # Project documentation (this file)
└── LICENSE                 # Project license (optional)
```

---

## **Key Functions**

### **1. `get_answer(messages)`**
Sends a conversation history (messages) to OpenAI's GPT-3.5-turbo model and receives a response. 

### **2. `speech_to_text(audio_data)`**
Converts an audio file (e.g., WAV, MP3) to text using OpenAI's Whisper model.

### **3. `text_to_speech(input_text)`**
Generates a speech (audio) file from a given text using OpenAI's Text-to-Speech model.

### **4. `autoplay_audio(file_path)`**
Automatically plays the audio response generated by the chatbot.

---

## **Dependencies**

You can install the dependencies using `pip`:

```bash
pip install streamlit openai python-dotenv audio-recorder-streamlit streamlit-float
```

Alternatively, you can use the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## **Known Issues**

- **Audio Quality**: The audio quality generated using OpenAI's TTS model may vary depending on the input and model settings.
- **Latency**: Depending on the network and API response time, there may be a slight delay between the user input and the chatbot’s response.

---

## **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for more details.

---

## **Acknowledgements**

- **OpenAI** for providing powerful APIs for natural language processing, speech-to-text, and text-to-speech.
- **Streamlit** for enabling easy web app development.
- **Audio Recorder Streamlit** for smooth integration of voice input functionality.

---

### **Contributing**

Feel free to fork this project, make improvements, and submit pull requests. Contributions are welcome!

