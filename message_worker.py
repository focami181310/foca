import json
import logging
import os

logger = logging.getLogger(__name__)

#Загрузка окружения .env. Получение ключа и модели из env
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("LLM_MODEL")

temperature = os.getenv("TEMP")
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

def send_message(name, content):
    with open('system_promt.json', 'r', encoding='utf-8') as f:
        system_promt = json.load(f)
    with open('dialog_history.json', 'r', encoding='utf-8') as f:
        dialog_history = json.load(f)
    
    messages =  [{"role": "system", "content": system_promt}] + dialog_history + [{"role": "user", "content": name+': '+content}]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response
