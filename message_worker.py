import json
import logging
import os
import foca_utils
from openai import BadRequestError
from dotenv import load_dotenv
from pathlib import Path

#Настройка логгера
time_format = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)

#Загрузка окружения .env. Получение ключа и модели из env
load_dotenv()

openai_api_key = os.getenv("LLM_OPENAI_API_KEY")
base_url = os.getenv("LLM_OPENAI_BASE_URL")
model = os.getenv("LLM_MODEL")

temperature = os.getenv("LLM_TEMPERATURE")
temperature = float(temperature)

max_tokens = os.getenv("LLM_MAX_TOKENS")
max_tokens = int(max_tokens)

#Подключение к провайдеру LLM
from openai import OpenAI
client = OpenAI(
    api_key=openai_api_key,
    base_url=base_url,

)

memory_dir = Path("memory")

#Функция добавления сообщения без отправки
def add_message(role, name, content):
    chat_history = json.loads(memory_dir.joinpath("chat_history.json").read_text(encoding="utf-8"))

    current_time = foca_utils.get_current_time()

    chat_history.append({
        "role": role,
        "content": f"{current_time}\n{name}: {content}"
    })

    chat_history_json = json.dumps(chat_history, ensure_ascii=False, indent=4)

    (memory_dir / "chat_history.json").write_text(chat_history_json, encoding="utf-8")


#Отправка сообщения и получение ответа
def send_message(name, content):
    system_prompt = json.loads(memory_dir.joinpath("system_promt.json").read_text(encoding="utf-8"))
    chat_history = json.loads(memory_dir.joinpath("chat_history.json").read_text(encoding="utf-8"))

    # Читаем обычный текстовый файл
    long_term_memory = memory_dir.joinpath("long_term_memory.md").read_text(encoding="utf-8")

    current_time = foca_utils.get_current_time()

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

    (memory_dir / "chat_history.json").write_text(chat_history_json, encoding="utf-8")

    return response
