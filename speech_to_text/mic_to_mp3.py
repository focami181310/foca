import os
import time
from scipy.io.wavfile import write
import sounddevice as sd
from constants import DATA_DIR

# 1. Прописываем путь к FFmpeg в PATH до импорта pydub (убирает RuntimeWarning)
ffmpeg_path = r"C:\ffmpeg\bin"
if ffmpeg_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + ffmpeg_path

# 2. Теперь импортируем pydub — предупреждения больше не будет
from pydub import AudioSegment

# Параметры записи
fs = 44100  # Частота дискретизации (44.1 кГц)
seconds = 5  # Длительность записи в секундах


def start_recording():
    print("Запись началась...")
    # Запись с микрофона
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Ожидание окончания записи
    print("Запись завершена.")

    # Временный WAV-файл
    wav_filename = "temp_audio.wav"

    # Формируем путь к MP3 и создаем папки, если их нет
    output_dir = DATA_DIR / "mic_audio"
    output_dir.mkdir(parents=True, exist_ok=True)
    mp3_filename = output_dir / f"recording{int(time.time())}.mp3"

    # Сохраняем WAV
    write(wav_filename, fs, myrecording)

    # Конвертируем WAV в MP3 через Pydub
    sound = AudioSegment.from_wav(wav_filename)
    sound.export(mp3_filename, format="mp3")

    # Удаляем временный WAV-файл
    os.remove(wav_filename)

    print(f"Файл сохранен")
    return mp3_filename
