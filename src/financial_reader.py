import os
from typing import Union

import pandas as pd


def read_financial_csv(file_path: str) -> list[dict]:
    """
    Считывает финансовые операции из CSV файла и возвращает список словарей

    Args:
        file_path (str): Полный путь к CSV файлу

    Returns:
        list[dict]: Список словарей с финансовыми операциями

    Raises:
        FileNotFoundError: Если файл не найден
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    df_csv = pd.read_csv(file_path)
    transactions_csv = df_csv.to_dict("records")

    return transactions_csv


def read_financial_excel(file_path: str, sheet_name: Union[str, int] = 0) -> list[dict]:
    """
    Считывает финансовые операции из Excel файла и возвращает список словарей

    Args:
        file_path (str): Полный путь к Excel файлу
        sheet_name (str, int): Название или индекс листа для чтения (по умолчанию 0 - первый лист)

    Returns:
        List[Dict]: Список словарей с финансовыми операциями

    Raises:
        FileNotFoundError: Если файл не найден
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    df = pd.read_excel(file_path, sheet_name=sheet_name)
    transactions_excel = df.to_dict("records")

    return transactions_excel
