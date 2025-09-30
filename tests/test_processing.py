import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data() -> list[dict]:
    """Фикстура с примером данных для тестирования фильтрации по состоянию."""
    return [
        {"state": "", "id": 0},
        {"state": "EXECUTED", "id": 1},
        {"state": "UNKNOWN", "id": 2},
        {"state": "CANCELED", "id": 3},
    ]


@pytest.mark.parametrize("state", ["EXECUTED", "PENDING", "CANCELED", "UNKNOWN"])
def test_filter_by_state_parameterized(sample_data: list[dict], state: str) -> None:
    """Тест функции filter_by_state c разными параметрами (истинными и ложными)"""
    result = filter_by_state(sample_data, state)
    assert all(item["state"] == state for item in result)


@pytest.fixture
def sample_dates() -> list[dict]:
    """Фикстура с примером данных для тестирования сортировки по дате."""
    return [
        {"date": "2023-01-15T10:30:00", "id": 1},
        {"date": "2023-03-20T14:45:00", "id": 2},
        {"date": "2023-02-10T08:15:00", "id": 3},
        {"date": "invalid-date-format", "id": 4},
        {"id": 2},
    ]


def test_sort_by_date_descending(sample_dates: list[dict]) -> None:
    """Тестирование функции sort_by_date (сначала новые даты)"""
    result = sort_by_date(sample_dates, reverse=True)
    expected = [
        {"date": "2023-03-20T14:45:00", "id": 2},
        {"date": "2023-02-10T08:15:00", "id": 3},
        {"date": "2023-01-15T10:30:00", "id": 1},
    ]
    assert result == expected


def test_sort_by_date_ascending(sample_dates_unsorted: list[dict]) -> None:
    """Тестирование функции sort_by_date (сначала старые даты)"""
    result = sort_by_date(sample_dates_unsorted, reverse=False)
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


def test_sort_by_date_invalid_format(sample_invalid_dates: list[dict]) -> None:
    """Тестирование обработки некорректного формата даты"""
    with pytest.raises(ValueError):
        sort_by_date(sample_invalid_dates)


def test_sort_by_date_missing_key(sample_missing_key: list[dict]) -> None:
    """Тестирование обработки отсутствующего ключа 'date'"""
    with pytest.raises(KeyError):
        sort_by_date(sample_missing_key)
