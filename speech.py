import os
from logger import logger
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from elevenlabs.client import ElevenLabs
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile
from io import BytesIO

# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY environment variable not set!")
if not ELEVENLABS_API_KEY:
    logger.error("ELEVENLABS_API_KEY environment variable not set!")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def listen_to_command():
    logger.info("Starting command listening process")
    try:
        # Record audio directly using sounddevice
        logger.info("Recording audio...")
        print("🎙️ Listening...")

        # Record 5 seconds of audio at 44.1kHz
        duration = 5
        fs = 44100
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        # Save audio to a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            scipy.io.wavfile.write(temp_file.name, fs, audio)

            # Read the WAV file and create a BytesIO object
            with open(temp_file.name, 'rb') as wav_file:
                audio_data = BytesIO(wav_file.read())

        # Convert speech to text using ElevenLabs
        logger.info("Transcribing with ElevenLabs...")
        print("📝 Transcribing...")

        transcription = client.speech_to_text.convert(
            file=audio_data,
            model_id="scribe_v1",  # Model to use
            tag_audio_events=True,  # Tag audio events like laughter, applause, etc.
            language_code="eng",    # Language of the audio file
            diarize=True           # Whether to annotate who is speaking
        )

        print(f"🗣️ Transcription: {transcription}")
        logger.info(f"Command processing completed - Transcription: '{transcription}'")
        return transcription

    except Exception as e:
        logger.error(f"Error in listen_to_command: {str(e)}")
        return None
    finally:
        # Clean up the temporary file
        if 'temp_file' in locals():
            try:
                os.unlink(temp_file.name)
                logger.info(f"Cleaned up temporary file: {temp_file.name}")
            except Exception as e:
                logger.error(f"Error cleaning up temporary file: {str(e)}")
