import logging
import message_worker
import voice_generator
from dotenv import load_dotenv
import os
import crash_check
from datetime import datetime
from memory.summarizer import summarize
from speech_to_text.voice_text import get_voice_text

#Настройка логгера
time_format = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)
logging.basicConfig(filename='foca.log',
                    level=logging.INFO,
                    format='%(asctime)s – %(message)s',
                    datefmt=time_format)

load_dotenv()

user_name = os.getenv("USER_NAME")
NORMAL_MESSAGE = f"{user_name} инициализировал попытку запустить мост..."
CRASH_MESSAGE = f"{user_name} инициализировал попытку запустить мост... Прошлая попытка не удалась..."
SKIP = "[пропуск]"


def main():
    logger.info('Starting Foca...')
    mute_state = False

    print(f"{user_name}: ", end='')

    #init message
    message = input()
    if "/mute @foca" in message:
        mute_state = True

    check = crash_check.previous_run_crashed()
    crash_check.create_crash_marker()

    if check:
        print("Мост: Попытка запустить мост... Прошлая попытка не удалась...")
        message_worker.add_message("user", "Мост", CRASH_MESSAGE)
    else:
        print("Мост: Попытка запустить мост...")
        response = message_worker.add_message("user", "Мост", NORMAL_MESSAGE)

    first = True

    while True:
        summarize_res = summarize()
        if summarize_res == "summarized":
            message_worker.add_message("user", "Уведомление", "Память обновлена")
            print("Уведомление: Память обновлена")
        logger.info(summarize_res)

        if message == '':
            response = message_worker.send_message(user_name, None)
        elif message == '/v':
            response = message_worker.send_message(user_name, "[Голосовое сообщение]" + get_voice_text())
        else:
            response = message_worker.send_message(user_name, message)

        if not response.choices[0].message.content == SKIP and not mute_state:
            audio_file = voice_generator.text_to_mp3_file(response.choices[0].message.content)

        print(f"\nФокалорс: {response.choices[0].message.content}\n")

        if not response.choices[0].message.content == SKIP and not mute_state:
            voice_generator.play_mp3(audio_file)

        print("Фоками: ", end = '')
        message = input()
        if "/mute @foca" in message:
            mute_state = True
        elif "/unmute @foca" in message:
            mute_state = False

        first = False

        if message == "exit":
            crash_check.remove_crash_marker()
            break


    logger.info('Stopping Foca...')


if __name__ == '__main__':
    main()
    