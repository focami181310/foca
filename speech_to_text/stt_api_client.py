from openai import OpenAI
import os
from constants import DATA_DIR
import logging

logger = logging.getLogger(__name__)

openai_api_key = os.getenv("STT_OPENAI_API_KEY")
base_url = os.getenv("STT_OPENAI_BASE_URL")
model = os.getenv("STT_MODEL")

client = OpenAI(
    api_key=openai_api_key,
    base_url=base_url,
)

def speech_to_text(audio_file):
    logger.info("stt start")
    with open(audio_file, "rb") as audio:
        transcript = client.audio.transcriptions.create(
            model=model,
            file=audio,
            language="ru"
        )
    logger.info("stt complete")
    return transcript.text
