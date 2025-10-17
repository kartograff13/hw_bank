import json
import os
from typing import Any


def load_transactions_file(file_path: str) -> list[dict[str, Any]]:
    """Функция загружает файл транзакций из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу с транзакциями

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями или пустой список
    """
    try:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return []
        with open(file_path, "r", encoding="utf-8") as file:
            data_transactions = json.load(file)

        return data_transactions if isinstance(data_transactions, list) else []

    except (json.JSONDecodeError, FileNotFoundError):
        return []
