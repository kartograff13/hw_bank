import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize("state", ["EXECUTED", "PENDING", "CANCELED", "UNKNOWN"])
def test_filter_by_state_parameterized(state: str) -> None:
    """Тест функции filter_by_state c разными параметрами (истинными и ложными)"""
    sample_data = [
        {"state": "", "id": 0},
        {"state": "EXECUTED", "id": 1},
        {"state": "UNKNOWN", "id": 2},
        {"state": "CANCELED", "id": 3},
    ]
    result = filter_by_state(sample_data, state)
    assert all(item["state"] == state for item in result)


def test_sort_by_date_descending() -> None:
    """Тестирование функции sort_by_date (сначала новые даты)"""
    sample_data = [
        {"date": "2023-01-15T10:30:00", "id": 1},
        {"date": "2023-03-20T14:45:00", "id": 2},
        {"date": "2023-02-10T08:15:00", "id": 3},
    ]
    result = sort_by_date(sample_data, reverse=True)
    expected = [
        {"date": "2023-03-20T14:45:00", "id": 2},
        {"date": "2023-02-10T08:15:00", "id": 3},
        {"date": "2023-01-15T10:30:00", "id": 1},
    ]
    assert result == expected


def test_sort_by_date_ascending() -> None:
    """Тестирование функции sort_by_date (сначала старые даты)"""
    sample_data = [
        {"date": "2023-03-20T14:45:00", "id": 1},
        {"date": "2023-01-15T10:30:00", "id": 2},
        {"date": "2023-02-10T08:15:00", "id": 3},
    ]
    result = sort_by_date(sample_data, reverse=False)
    expected = [
        {"date": "2023-01-15T10:30:00", "id": 2},
        {"date": "2023-02-10T08:15:00", "id": 3},
        {"date": "2023-03-20T14:45:00", "id": 1},
    ]
    assert result == expected


def test_sort_by_date_empty_list() -> None:
    """Тестирование сортировки пустого списка"""
    result = sort_by_date([], reverse=True)
    assert result == []


def test_sort_by_date_single_element() -> None:
    """Тестирование сортировки списка с одним элементом"""
    sample_data = [{"date": "2023-01-15T10:30:00", "id": 1}]
    result = sort_by_date(sample_data, reverse=True)
    assert result == sample_data


def test_sort_by_date_invalid_format() -> None:
    """Тестирование обработки некорректного формата даты"""
    sample_data = [
        {"date": "2023-01-15T10:30:00", "id": 1},
        {"date": "invalid-date-format", "id": 2},
        {"date": "2023-02-10T08:15:00", "id": 3},
    ]

    with pytest.raises(ValueError):
        sort_by_date(sample_data)


def test_sort_by_date_missing_date_key() -> None:
    """Тестирование обработки отсутствующего ключа 'date'"""
    sample_data = [
        {"date": "2023-01-15T10:30:00", "id": 1},
        {"id": 2},  # type: ignore
        {"date": "2023-02-10T08:15:00", "id": 3},
    ]

    with pytest.raises(KeyError):
        sort_by_date(sample_data)  # type: ignore
