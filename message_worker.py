import json
import logging
import os
from openai import BadRequestError
from dotenv import load_dotenv
from constants import MEMORY_FILES_DIR
from datetime import datetime

def get_current_time():
    current_time = datetime.now()
    return current_time.strftime("%d.%m.%Y %H:%M:%S")

#Настройка логгера
time_format = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)

#Загрузка окружения .env. Получение ключа и модели из env
load_dotenv()

openai_api_key = os.getenv("LLM_OPENAI_API_KEY")
base_url = os.getenv("LLM_OPENAI_BASE_URL")
model = os.getenv("LLM_MODEL")

temperature = os.getenv("LLM_TEMPERATURE")
if temperature:
    temperature = float(temperature)

max_tokens = os.getenv("LLM_MAX_TOKENS")
if max_tokens:
    max_tokens = int(max_tokens)

#Подключение к провайдеру LLM
from openai import OpenAI
client = OpenAI(
    api_key=openai_api_key,
    base_url=base_url,

)

MEMORY_FILES_DIR.mkdir(parents=True, exist_ok=True)

#Функция добавления сообщения без отправки
def add_message(role, name, content):
    chat_history = json.loads(MEMORY_FILES_DIR.joinpath("chat_history.json").read_text(encoding="utf-8"))

    current_time = get_current_time()

    chat_history.append({
        "role": role,
        "name": name,
        "content": f"[{current_time}] - {content}"
    })

    chat_history_json = json.dumps(chat_history, ensure_ascii=False, indent=4)

    (MEMORY_FILES_DIR / "chat_history.json").write_text(chat_history_json, encoding="utf-8")


#Отправка сообщения и получение ответа
def send_message(name, content):
    system_prompt = json.loads(MEMORY_FILES_DIR.joinpath("system_prompt.json").read_text(encoding="utf-8"))
    chat_history = json.loads(MEMORY_FILES_DIR.joinpath("chat_history.json").read_text(encoding="utf-8"))

    # Читаем обычный текстовый файл
    long_term_memory = MEMORY_FILES_DIR.joinpath("long_term_memory.md").read_text(encoding="utf-8")

    current_time = get_current_time()

    combined_system_content = f"{system_prompt}\n\n[ДОЛГОВРЕМЕННАЯ ПАМЯТЬ]\n{long_term_memory}\n\n[ТЕКУЩЕЕ ВРЕМЯ]: {current_time}"

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

    chat_history_json = json.dumps(chat_history, ensure_ascii=False, indent=4)

    (MEMORY_FILES_DIR / "chat_history.json").write_text(chat_history_json, encoding="utf-8")

    return response
