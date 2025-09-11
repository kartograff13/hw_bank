from typing import Any, Dict


def filter_by_state(data: list[Dict[str, Any]], state: str = "EXECUTED") -> list[Dict[str, Any]]:
    """
    Фильтрует список словарей содержащий только значения ключа "state".

    Args:
        data: Список словарей для фильтрации
        state: Значение состояния для фильтрации (по умолчанию "EXECUTED")

    Returns:
        Отфильтрованный список словарей, у которых ключ "state" соответствует заданному значению
    """
    return list(filter(lambda item: item.get("state") == state, data))
