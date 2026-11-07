import logging
import message_worker
import voice_generator
from dotenv import load_dotenv
import os
import crush_check

#Настройка логгера
time_format = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)
logging.basicConfig(filename='foca.log',
                    level=logging.INFO,
                    format='%(asctime)s – %(message)s',
                    datefmt=time_format)

load_dotenv()

username = os.getenv("USERNAME")
NORMAL_MESSAGE = f"{username} инициализировал попытку запустить мост..."
CRUSH_MESSAGE = f"{username} инициализировал попытку запустить мост... Прошлая попытка не удалась..."
SKIP = "[пропуск]"


def main():
    logger.info('Starting Foca...')

    check = crush_check.previous_run_crushed()

    if check:
        print("Мост: Попытка запустить мост... Прошлая попытка не удалась...")
        response = message_worker.send_message("Мост", CRUSH_MESSAGE)
    else:
        print("Мост: Попытка запустить мост...")
        response = message_worker.send_message("Мост", NORMAL_MESSAGE)

    first = True

    while True:
        if not first:
            response = message_worker.send_message(username, message)
        else:
            print("\nМост: Мост был запущен. На другом конце Фока.\n")

        if not response.choices[0].message.content == SKIP:
            audio_file = voice_generator.text_to_mp3_file(response.choices[0].message.content)

        print(f"\nФокалорс: {response.choices[0].message.content}\n")

        if not response.choices[0].message.content == SKIP:
            voice_generator.play_mp3(audio_file)

        print("Фоками: ", end = '')
        message = input()

        first = False
        
        if message == "exit":
            crush_check.remove_crash_marker()
            break


    logger.info('Stopping Foca...')


if __name__ == '__main__':
    main()
    