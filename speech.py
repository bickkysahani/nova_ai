import whisper
import sounddevice as sd
import numpy as np
import tempfile
import os
from logger import logger
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Get API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY environment variable not set!")

logger.info("Loading Whisper model...")
model = whisper.load_model("base")
logger.info("Whisper model loaded successfully")

def record_audio(duration=5, fs=44100):
    logger.info(f"Starting audio recording for {duration} seconds at {fs}Hz")
    print("🎙️ Listening...")
    try:
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        logger.info("Audio recording completed successfully")
        return np.squeeze(audio)
    except Exception as e:
        logger.error(f"Error during audio recording: {str(e)}")
        raise

def save_audio(audio, fs):
    logger.info("Saving audio to temporary file")
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            import scipy.io.wavfile
            scipy.io.wavfile.write(f.name, fs, audio)
            logger.info(f"Audio saved to temporary file: {f.name}")
            return f.name
    except Exception as e:
        logger.error(f"Error saving audio file: {str(e)}")
        raise

def transcribe_audio(path):
    logger.info(f"Starting audio transcription for file: {path}")
    print("📝 Transcribing with Whisper...")
    try:
        result = model.transcribe(path)
        logger.info("Transcription completed successfully")
        return result["text"]
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        raise

def improve_transcription(text):
    logger.info("Starting transcription improvement with GPT")
    print("🤖 Sending to GPT for cleanup...")
    try:
        # Initialize the LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            api_key=OPENAI_API_KEY
        )

        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an assistant that improves voice command transcriptions.
Make sure the command is corrected for clarity and meaning."""),
            ("user", "Original: {text}\nImproved:")
        ])

        # Create the chain
        chain = prompt | llm

        # Process the text
        improved_text = chain.invoke({"text": text}).content.strip()

        logger.info("Transcription improvement completed successfully")
        return improved_text
    except Exception as e:
        logger.error(f"Error during transcription improvement: {str(e)}")
        raise

def listen_to_command():
    logger.info("Starting command listening process")
    try:
        audio = record_audio()
        path = save_audio(audio, 44100)
        raw = transcribe_audio(path)
        clean = improve_transcription(raw)
        print(f"🗣️ Raw: {raw}")
        print(f"✨ Cleaned: {clean}")
        logger.info(f"Command processing completed - Raw: '{raw}', Cleaned: '{clean}'")
        return clean
    except Exception as e:
        logger.error(f"Error in listen_to_command: {str(e)}")
        return None
    finally:
        # Clean up temporary files
        if 'path' in locals():
            try:
                os.unlink(path)
                logger.info(f"Cleaned up temporary file: {path}")
            except Exception as e:
                logger.error(f"Error cleaning up temporary file: {str(e)}")
