import json
import logging
import os
import foca_utils
from openai import BadRequestError
from dotenv import load_dotenv

#Настройка логгера
time_format = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)

#Загрузка окружения .env. Получение ключа и модели из env
load_dotenv()

openai_api_key = os.getenv("LLM_OPENAI_API_KEY")
base_url = os.getenv("LLM_OPENAI_BASE_URL")
model = os.getenv("LLM_MODEL")

temperature = os.getenv("LLM_TEMPERATURE")
if temperature is None or temperature == '':
    logger.warning("Не задана temperature для LLM. По умолчанию (0.8)")
    print("Предупреждение: Не задана температура для LLM в файле .env! Установлено значение по умолчанию (0.8)")
    temperature = "0.8"
temperature = float(temperature)

max_tokens = os.getenv("LLM_MAX_TOKENS")
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

#Функция добавления сообщения без отправки
def add_message(role, name, content):
    with open("chat_history.json", 'r', encoding='utf-8') as f:
        chat_history = json.load(f)

    current_time = foca_utils.get_current_time()

    chat_history.append({
        "role": role,
        "content": f"{current_time}\n{name}: {content}"
    })

    with open("chat_history.json", 'w', encoding='utf-8') as f:   
        json.dump(chat_history, f, ensure_ascii=False, indent=4)



#Отправка сообщения и получение ответа
def send_message(name, content):
    with open("system_promt.json", 'r', encoding='utf-8') as f:
        system_promt = json.load(f)
    with open("chat_history.json", 'r', encoding='utf-8') as f:
        chat_history = json.load(f)
    with open("long_term_memory.md", 'r', encoding='utf-8') as f:
        long_term_memory = f.read()

    current_time = foca_utils.get_current_time()

    combined_system_content = f"{system_promt}\n\n[ДОЛГОВРЕМЕННАЯ ПАМЯТЬ]\n{long_term_memory}\n\n[ТЕКУЩЕЕ ВРЕМЯ]: {current_time}"

    if content!=None:    
        messages = [
            {
                "role": "system",
                "content": combined_system_content
            }
        ] + chat_history + [
            {
                "role": "user", 
                "name": name,
                "content": content
            }
        ]

        chat_history.append({
            "role": "user",
            "name": name,
            "content": f"[{current_time}] - {content}"
        })
    else:
        messages = [
            {
                "role": "system",
                "content": combined_system_content
            }
        ] + chat_history

    try:
#        if model == 'anthropic/claude-sonnet-5-5': 
#            logger.info(f"Main LLM: {model}")
#            logger.info(f"Temperature: {temperature}")
#            logger.info(f"Max tokens: {max_tokens}")
#            response = client.chat.completions.create(
#                model=model,
#                messages=messages,
#                temperature=temperature,
#                max_tokens=max_tokens
#            )
        if model == "deepseek/deepseek-v4.1-flash-1017":
            logger.info(f"Main LLM: {model}")
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                extra_body={"thinking": {"type": "disabled"}},
            )
        else:
            logger.error("Поддерживается только deepseek/deepseek-v4.1-flash-1017")
            return None
    except BadRequestError as e:
        logger.error("Error API: %s", e)
        logger.error("Error of server: %s", e.response.text)
        raise

    response_text = response.choices[0].message.content
    chat_history.append({
        "role": "assistant",
        "name": "Focalors",
        "content": response_text
    })

    with open("chat_history.json", 'w', encoding='utf-8') as f:   
        json.dump(chat_history, f, ensure_ascii=False, indent=4)

    return response
