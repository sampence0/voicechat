import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def transcribe_audio(audio_path):
    with open(audio_path, 'rb') as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    print(transcript)  # You can remove this line if you don't want to print the API response anymore

    return transcript['text']  # Change this line to return the correct value


if __name__ == "__main__":
    transcribed_text = transcribe_audio('output.wav')
    print(transcribed_text)
