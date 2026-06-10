import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Функция выполняет поиск банковских операций и фильтрует список по совпадению в описании"""
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [
        operation for operation in data if operation.get("description") and pattern.search(operation["description"])
    ]


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Подсчитывает количество операций по заданным категориям"""
    descriptions = [operation.get("description", "").lower() for operation in data]

    return {category: sum(1 for desc in descriptions if category.lower() in desc) for category in categories}
