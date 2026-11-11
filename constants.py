import pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"

CACHE_DIR = PROJECT_ROOT / "cache"

MEMORY_FILES_DIR = PROJECT_ROOT / "data" / "memory"

MEMORY_BACKUP_DIR = PROJECT_ROOT / "data" / "memory" / "backups"
