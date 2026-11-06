import logging
import message_worker

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

    print("Мост: Мост был запущен. На другом конце Фока.")
    response = message_worker.send_message("Мост", f"Мост был запущен. На другом конце {username}.")
    print(f"\nФокалорс: {response.choices[0].message.content}\n")

    while True:
        print("Фоками: ", end = '')
        message = input()
        
        if message == "exit":
            break

        response = message_worker.send_message(username, message)
        print(f"\nФокалорс: {response.choices[0].message.content}\n")

    logger.info('Stopping Foca...')


if __name__ == '__main__':
    main()
    