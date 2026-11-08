from speech_to_text.mic_to_mp3 import start_recording
from speech_to_text.stt_api_client import speech_to_text

def get_voice_text():
    return speech_to_text(start_recording())