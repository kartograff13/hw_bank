import os
from typing import Optional, Union

import pandas as pd


def safe_str(value: Optional[Union[str, int, float]]) -> Optional[str]:
    """Безопасно преобразует значение в строку, обрабатывая особые случаи"""
    if value is None:
        return None

    if isinstance(value, float) and value != value:
        return None

    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return str(value)

    return str(value)


def _transform_transaction_row(row: dict) -> dict:
    """Преобразует строку транзакции из CSV/Excel в формат JSON"""

    return {
        "id": row.get("id"),
        "state": row.get("state"),
        "date": row.get("date"),
        "operationAmount": {
            "amount": str(row.get("amount")) if row.get("amount") is not None else "0",
            "currency": {"name": row.get("currency_name"), "code": row.get("currency_code")},
        },
        "description": row.get("description"),
        "from": safe_str(row.get("from")),
        "to": safe_str(row.get("to")),
    }


def read_financial_csv(file_path: str) -> list[dict]:
    """
    Считывает финансовые операции из CSV-файла и возвращает список словарей

    Args:
        file_path (str): Полный путь к CSV-файлу

    Returns:
        list[dict]: Список словарей с финансовыми операциями

    Raises:
        FileNotFoundError: Если файл не найден
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    df_csv = pd.read_csv(file_path, sep=";")
    transactions_csv = df_csv.to_dict("records")
    transformed_transactions = [_transform_transaction_row(row) for row in transactions_csv]

    return transformed_transactions


def read_financial_excel(file_path: str, sheet_name: Union[str, int] = 0) -> list[dict]:
    """
    Считывает финансовые операции из Excel-файла и возвращает список словарей

    Args:
        file_path (str): Полный путь к Excel-файлу
        sheet_name (str, int): Название или индекс листа для чтения (по умолчанию 0 - первый лист)

    Returns:
        list[dict]: Список словарей с финансовых операций

    Raises:
        FileNotFoundError: Если файл не найден
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    df = pd.read_excel(file_path, sheet_name=sheet_name)
    transactions_excel = df.to_dict("records")
    transformed_transactions = [_transform_transaction_row(row) for row in transactions_excel]

    return transformed_transactions
