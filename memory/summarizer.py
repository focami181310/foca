from openai import OpenAI, BadRequestError
import logging
from dotenv import load_dotenv
import os
import json
from constants import MEMORY_FILES_DIR
from memory.memory_manager import memory_backup

logger = logging.getLogger(__name__)

load_dotenv()
openai_api_key = os.getenv("SUMMARIZER_OPENAI_API_KEY")
base_url = os.getenv("SUMMARIZER_OPENAI_BASE_URL")
model = os.getenv("SUMMARIZER_MODEL")

client = OpenAI(
    api_key=openai_api_key,
    base_url=base_url,
)

MAX_MESSAGES = int(os.getenv("MAX_MESSAGES"))
KEEP_MESSAGES = int(os.getenv("KEEP_MESSAGES"))

def trim_history(messages):
    if len(messages) > MAX_MESSAGES:
        messages = messages[-KEEP_MESSAGES:]
        while messages and messages[0]["role"] != "user":
            messages = messages[1:]
    return messages

def summarize():
    summarizer_system_prompt = json.loads(MEMORY_FILES_DIR.joinpath("summarizer_prompt.json").read_text(encoding="utf-8"))
    chat_history = json.loads(MEMORY_FILES_DIR.joinpath("chat_history.json").read_text(encoding="utf-8"))
    if len(chat_history) <= MAX_MESSAGES:
        return f"{MAX_MESSAGES - len(chat_history)} before summarizing"

    #делаем bachup памяти перед перезаписью
    memory_backup_res = memory_backup()
    if memory_backup_res:
        return memory_backup_res
    print("Уведомление: Память начинает обновляться... Пожалуйста, подождите...")
    logger.info("Starting summarizing")
    long_term_memory = MEMORY_FILES_DIR.joinpath("long_term_memory.md").read_text(encoding="utf-8")

    combined_system_content = f"{summarizer_system_prompt}\n\n[ДОЛГОВРЕМЕННАЯ ПАМЯТЬ]\n{long_term_memory}\n\n[ПОСЛЕДНЯЯ ИСТОРИЯ ЧАТА]\n{chat_history}"
   
    messages = [
        {
            "role": "system",
            "content": combined_system_content
        }
    ]
    logger.info(f"Summarizing using LLM: {model}")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
    except BadRequestError as e:
        logger.error("Error API: %s", e)
        logger.error("Error of server: %s", e.response.text)
        raise

    response_text = response.choices[0].message.content

    (MEMORY_FILES_DIR / "long_term_memory.md").write_text(response_text, encoding="utf-8")

    chat_history = trim_history(chat_history)

    chat_history_json = json.dumps(chat_history, ensure_ascii=False, indent=4)

    (MEMORY_FILES_DIR / "chat_history.json").write_text(chat_history_json, encoding="utf-8")

    return "summarized"
