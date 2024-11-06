
import os
import base64
import streamlit as st
import boto3
import requests
import json
import time
from dotenv import load_dotenv
load_dotenv()

# # AWS Credentials (stored in your environment variables or setup with AWS CLI)
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

# AWS clients for Polly, Transcribe, and Bedrock
polly_client = boto3.client('polly')
transcribe_client = boto3.client('transcribe')
bedrock_client = boto3.client('bedrock-runtime')
s3_client = boto3.client('s3')

BUCKET_NAME = 'audiotextbkt'

# Function to upload file to S3 for transcription
def upload_to_s3(file_path, job_name):
    s3_client.upload_file(file_path, BUCKET_NAME, f'{job_name}.wav')
# Function to process user query using AWS Bedrock
def get_answer(query):
    try:
        prompt =str(query)
        formatted_prompt = f"<s>[INST] {prompt} [/INST]"
        # Construct the request payload with the correct structure
        native_request = {
            "prompt": formatted_prompt,
            "max_tokens": 512,  # Maximum number of tokens in the response
            "temperature": 0.5  # Control the randomness of the response
        }

        # Model ID for Bedrock
        model_id = "mistral.mistral-large-2402-v1:0"

        # Convert request to JSON format
        request = json.dumps(native_request)

        # Invoke the model using AWS Bedrock
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=request,
            #accept='application/json',
            #contentType='application/json'
        )
        # Read the response body and parse it as JSON
        response_body = json.loads(response['body'].read().decode('utf-8'))
        # Extract the generated response from the model
        if "outputs" in response_body and len(response_body["outputs"]) > 0:
            bot_response = response_body["outputs"][0]["text"]
            return bot_response
        else:
            return "Error: 'outputs' key not found or is empty in the response."

    except Exception as e:
        return f"Error processing query: {str(e)}"

# Speech-to-text using AWS Transcribe

def speech_to_text(audio_file_path):
    # Upload the audio file to S3
    bucket_name = 'audiobktchat'  # Replace with your S3 bucket name
    s3_file_path = os.path.basename(audio_file_path)

    try:
        # Upload the file to S3
        s3_client.upload_file(audio_file_path, bucket_name, s3_file_path)

        # Construct the S3 URI
        media_file_uri = f's3://{bucket_name}/{s3_file_path}'
        job_name = f"transcription-job-{int(time.time())}"

        # job_name = "transcription-job"
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": media_file_uri},
            MediaFormat="mp3",  # Adjust if your audio file format is different
            LanguageCode="en-US",
        )

        # Wait for the job to complete
        while True:
            result = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            if result['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
                transcript_url = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
                transcript = requests.get(transcript_url).json()
                return transcript['results']['transcripts'][0]['transcript']
            elif result['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
                return "Error: Transcription job failed."
            else:
                time.sleep(5)  # Wait before checking again

    except Exception as e:
        return f"Error processing audio file: {str(e)}"


def text_to_speech(input_text):
    # Call AWS Polly to convert text to speech
    response = polly_client.synthesize_speech(
        Text=input_text,
        OutputFormat='mp3',
        VoiceId='Joanna'  # Choose your desired voice
    )
    audio_file_path = 'temp_audio_play.mp3'
    with open(audio_file_path, 'wb') as f:
        f.write(response['AudioStream'].read())
    return audio_file_path

# Autoplay audio in Streamlit
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

# Example usage
if __name__ == "__main__":
    st.title("AWS-Based Chatbot with Voice Features")

    # User input
    user_message = st.text_input("Type your question:")

    if user_message:
        # Get the chatbot response from AWS Bedrock
        answer = get_answer(user_message)
        st.write(answer)

        # Convert the text answer to speech using AWS Polly
        audio_path = text_to_speech(answer)
        # Play the generated audio
        autoplay_audio(audio_path)
