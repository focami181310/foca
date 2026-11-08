from openai import OpenAI
import os
from constants import DATA_DIR

openai_api_key = os.getenv("TTS_OPENAI_API_KEY")
base_url = os.getenv("TTS_OPENAI_BASE_URL")
model = os.getenv("TTS_MODEL")

client = OpenAI(
    api_key=openai_api_key,
    base_url=base_url,
)

def speech_to_text(audio_file):
    print("stt start")
    with open(DATA_DIR / "mic_audio" / audio_file, "rb") as audio:
        transcript = client.audio.transcriptions.create(
            model="openai/whisper-large-v3-turbo",
            file=audio,
            language="ru"
        )
    print("stt complete")
    return transcript.text
