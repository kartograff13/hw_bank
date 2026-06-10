import json
import logging
import os
from typing import Any

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
log_dir = os.path.join(project_root, "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "transactions_logger.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file, mode="w", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


def load_transactions_file() -> list[dict[str, Any]]:
    """Функция загружает файл транзакций из JSON-файла.

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями или пустой список
    """
    logger.info("Начало загрузки файла транзакций...")

    file_path = os.path.join(project_root, "data", "operations.json")

    try:
        if not os.path.exists(file_path):
            logger.error(f"Файл не найден: {file_path}")
            return []

        if os.path.getsize(file_path) == 0:
            logger.warning(f"Файл пуст: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data_transactions = json.load(file)

        result = data_transactions if isinstance(data_transactions, list) else []
        logger.info(f"Успешно загружено {len(result)} транзакций")
        return result

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при загрузке файла: {e}")
        return []
