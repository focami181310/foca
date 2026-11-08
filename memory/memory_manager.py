import shutil
from constants import MEMORY_FILES_DIR, MEMORY_BACKUP_DIR
from datetime import datetime
from pathlib import Path 
import logging

logger = logging.getLogger(__name__)

def memory_files_check():
    if not Path.exists(MEMORY_FILES_DIR/"system_prompt.json"):
        logger.error("system_prompt.json does not exist!")
        print("ERROR: system_prompt.json does not exist!")
        return "system_prompt.json does not exist!"

    if not Path.exists(MEMORY_FILES_DIR/"chat_history.json"):
        logger.error("chat_history.json does not exist!")
        print("ERROR: chat_history.json does not exist!")
        return "chat_history.json does not exist!"
    
    if not Path.exists(MEMORY_FILES_DIR/"long_term_memory.md"):
        logger.error("long_term_memory.md does not exist!")
        print("ERROR: long_term_memory.md does not exist!")
        return "long_term_memory.md does not exist!"
    
    return 0

def memory_backup_check(time):
    if not Path.exists(MEMORY_BACKUP_DIR / time / "system_prompt.json"):
        logger.error("system_prompt.json BACKUP does not exist!")
        print("ERROR: system_prompt.json BACKUP does not exist!")
        return "system_prompt.json BACKUP does not exist!"

    if not Path.exists(MEMORY_BACKUP_DIR / time / "chat_history.json"):
        logger.error("chat_history.json BACKUP does not exist!")
        print("ERROR: chat_history.json BACKUP does not exist!")
        return "chat_history.json BACKUP does not exist!"
    
    if not Path.exists(MEMORY_BACKUP_DIR/ time / "long_term_memory.md"):
        logger.error("long_term_memory.md BACKUP does not exist!")
        print("ERROR: long_term_memory.md BACKUP does not exist!")
        return "long_term_memory.md BACKUP does not exist!"
    
    return 0

def get_current_time():
    current_time = datetime.now()
    return current_time.strftime("%Y-%m-%d-%H-%M-%S")

def memory_backup():
    mfcheck_res = memory_files_check()

    if mfcheck_res:
        return mfcheck_res

    current_time = get_current_time()
    
    backup_path = MEMORY_BACKUP_DIR / current_time
    backup_path.mkdir(parents=True, exist_ok=True)

    shutil.copy(MEMORY_FILES_DIR/"system_prompt.json", backup_path/"system_prompt.json")
    shutil.copy(MEMORY_FILES_DIR/"chat_history.json", backup_path/"chat_history.json")
    shutil.copy(MEMORY_FILES_DIR/"long_term_memory.md", backup_path/"long_term_memory.md")

    mbcheck_res = memory_backup_check(current_time)
    if mbcheck_res:
        return mbcheck_res

    return 0
