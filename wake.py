import pvporcupine
import pyaudio
import struct
import os
from dotenv import load_dotenv
from logger import logger

load_dotenv()

def detect_wake_word():
    access_key = os.getenv('PICOVOICE_ACCESS_KEY')
    if not access_key:
        raise ValueError("Please set the PICOVOICE_ACCESS_KEY environment variable")

    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=["assets/hey-nova.ppn"]
    )
    pa = pyaudio.PyAudio()

    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )

    logger.info("Listening for 'Hey Nova'...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if porcupine.process(pcm) >= 0:
                logger.info("Wake word detected!")
                break
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()
