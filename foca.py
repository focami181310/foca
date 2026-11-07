import logging
import message_worker
import voice_generator

#Настройка логгера
time_format = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)
logging.basicConfig(filename='foca.log',
                    level=logging.INFO,
                    format='%(asctime)s – %(message)s',
                    datefmt=time_format)

username = "Фоками"

def main():
    logger.info('Starting Foca...')

    print("Мост: Попытка запустить мост...")
    response = message_worker.send_message("Мост", f"{username} инициализировал попытку запустить мост...")

    print("Мост: Мост был запущен. На другом конце Фока.")
    first = True

    while True:
        if not first:
            response = message_worker.send_message(username, message)

        audio_file = voice_generator.text_to_mp3_file(response.choices[0].message.content)
        print(f"\nФокалорс: {response.choices[0].message.content}\n")
        voice_generator.play_mp3(audio_file)

        print("Фоками: ", end = '')
        message = input()

        first = False
        
        if message == "exit":
            break


    logger.info('Stopping Foca...')


if __name__ == '__main__':
    main()
    