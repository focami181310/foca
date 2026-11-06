import os
import logging
import message_worker

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='foca.log', level=logging.INFO)
    logger.info('Starting Foca...')

    response = message_worker.send_message("Фоками", "Привет!")

    print(response.choices[0].messege.content)

    logger.info('Stopping Foca...')


if __name__ == '__main__':
    main()
    