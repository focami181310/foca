import json
import logging
import os
from datetime import datetime
from openai import BadRequestError

#Настройка логгера
time_format = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)
logging.basicConfig(filename='foca.log',
                    level=logging.INFO,
                    format='%(asctime)s – %(message)s',
                    datefmt=time_format)

#Загрузка окружения .env. Получение ключа и модели из env
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("LLM_MODEL")

temperature = os.getenv("LLM_TEMPERATURE")
if temperature is None or temperature == '':
    logger.warning("Не задана temperature для LLM. По умолчанию (0.8)")
    print("Предупреждение: Не задана температура для LLM в файле .env! Установлено значение по умолчанию (0.8)")
    temperature = "0.8"
temperature = float(temperature)

max_tokens = os.getenv("MAX_TOKENS")
if max_tokens is None or max_tokens == '':
    logger.warning("Не задана max_tokens для LLM. По умолчанию (300)")
    print("Предупреждение: Не задана max_tokens для LLM в файле .env! Установлено значение по умолчанию (300)")
    max_tokens = "300"
max_tokens = int(max_tokens)

#Подключение к провайдеру LLM
from openai import OpenAI
client = OpenAI(
    api_key=openai_api_key,
    base_url=base_url,

)

#Функция для получения времени сообщения
def get_current_time():
    current_time = datetime.now()
    return current_time.strftime("%d.%m.%Y %H:%M:%S")

#Отправка сообщения и получение ответа
def send_message(name, content):
    with open("C:\\Users\\focami\\Projects\\foca\\system_promt.json", 'r', encoding='utf-8') as f:
        system_promt = json.load(f)
    with open("C:\\Users\\focami\\Projects\\foca\\dialog_history.json", 'r', encoding='utf-8') as f:
        dialog_history = json.load(f)
    with open("C:\\Users\\focami\\Projects\\foca\\long_term_memory.md", 'r', encoding='utf-8') as f:
        long_term_memory = f.read()

    current_time = get_current_time()
    
    messages = [system_promt] + [
        {
            "role": "system",
            "content": long_term_memory
        }
    ] + dialog_history + [
        {
            "role": "user", 
             "content": f"Текущее время: {current_time}\n{name}: {content}"
        }
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
    except BadRequestError as e:
        logger.error("Ошибка API: %s", e)
        logger.error("Ответ сервера: %s", e.response.text)
        raise

    response_text = response.choices[0].message.content

    dialog_history.append({
        "role": "user",
        "content": f"{current_time}\n{name}: {content}"
    })

    dialog_history.append({
        "role": "assistant",
        "content": response_text
    })

    with open("C:\\Users\\focami\\Projects\\foca\\dialog_history.json", 'w', encoding='utf-8') as f:   
        json.dump(dialog_history, f, ensure_ascii=False, indent=4)

    return response
