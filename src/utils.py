import json
import os
from typing import Any


def load_transactions_file() -> list[dict[str, Any]]:
    """Функция загружает файл транзакций из JSON-файла.

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями или пустой список
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    file_path = os.path.join(project_root, 'data', 'operations.json')

    try:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return []
        with open(file_path, "r", encoding="utf-8") as file:
            data_transactions = json.load(file)

        return data_transactions if isinstance(data_transactions, list) else []

    except (json.JSONDecodeError, FileNotFoundError):
        return []
