import logging
import message_worker as mw
import voice_generator as vg
from dotenv import load_dotenv
import os
import crash_check as cr
from datetime import datetime
from memory.summarizer import summarize
from speech_to_text.voice_text import get_voice_text
from logging.handlers import RotatingFileHandler
from vision import img_in_message
import command_manager as cm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler = RotatingFileHandler('foca.log', maxBytes=2 * 1024 * 1024, backupCount=5, encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)



load_dotenv()

user_name = os.getenv("USER_NAME")
NORMAL_MESSAGE = f"{user_name} инициализировал попытку запустить мост..."
CRASH_MESSAGE = f"{user_name} инициализировал попытку запустить мост... Прошлая попытка не удалась..."
SKIP = "[пропуск]"


def main():
    logger.info('Starting Foca...')
    mute_state = False

    check = cr.previous_run_crashed()
    cr.create_crash_marker()

    if check:
        print("Мост: Попытка запустить мост... Прошлая попытка не удалась...")
        mw.add_message("user", "Мост", CRASH_MESSAGE)
    else:
        print("Мост: Попытка запустить мост...")
        response = mw.add_message("user", "Мост", NORMAL_MESSAGE)
    
    while True:
        print(f"{user_name}: ", end='')

        message = input()
        if "/mute @foca" in message:
            mute_state = True
            print("Foca was muted")
            continue
        elif "/unmute @foca" in message:
            mute_state = False
            print("Foca was unmuted")
            continue
        
        if message in cm.COMMANDS:
            response_text = cm.COMMANDS[message]()
        elif message == "/exit":
            mw.add_message("user", "Мост", f"{user_name} отключил мост")
            break
        else:
            mw.add_message("user", user_name, message)
            response_text = mw.send_message()

        if response_text != SKIP and not mute_state:
            audio_file = vg.text_to_mp3_file(response_text)

        print(f"\nFoca: {response_text}\n")

        if response_text != SKIP and not mute_state:
            vg.play_mp3(audio_file)

        summarize_res = summarize()
        if summarize_res == "summarized":
            mw.add_message("user", "Notification", "Memory was summarized")
            print("Notification: Memory was summarized")
        logger.info(summarize_res)
    
    print("Мост: мост был отключен")
    logger.info('Stopping Foca...')


if __name__ == '__main__':
    main()
    
