from openai import OpenAI
import os
import pygame
from dotenv import load_dotenv
import time

#загрузка параметров из .env
load_dotenv()

openai_api_key = os.getenv("VOICE_GEN_OPENAI_API_KEY")
base_url = os.getenv("VOICE_GEN_OPENAI_BASE_URL")
model = os.getenv("VOICE_GEN_MODEL")
voice = os.getenv("VOICE_ID")

client = OpenAI(
    api_key=openai_api_key,
    base_url=base_url,
)

def text_to_mp3_file(text):
    speech = client.audio.speech.create(
        model=model,
        input=text,
        voice=voice,
    )

    file_path = f"speech_{int(time.time())}.mp3"

    speech.write_to_file(file_path)
    return file_path

def play_mp3(audio_file):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()