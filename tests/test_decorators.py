from pathlib import Path

import pytest

from src.decorators import log


def test_log_success_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестирует логирование успешного выполнения в консоль"""

    @log()
    def test_func(x: int, y: int) -> int:
        return x + y

    result = test_func(2, 3)

    assert result == 5

    captured = capsys.readouterr()
    assert captured.out == "test_func ok\n"


def test_log_error_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестирует логирование ошибки в консоль"""

    @log()
    def test_func() -> None:
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        test_func()

    captured = capsys.readouterr()
    assert "test_func error: ValueError. Inputs: (), {}\n" in captured.out


def test_log_success_file(tmp_path: Path) -> None:
    """Тестирует логирование успешного выполнения в файл"""
    filename: Path = tmp_path / "test_log.txt"

    @log(filename=str(filename))
    def test_func(a: int, b: int, c: int = 10) -> int:
        return a + b + c

    result: int = test_func(1, 2, c=3)

    assert result == 6
    assert filename.read_text() == "test_func ok\n"


def test_log_error_file(tmp_path: Path) -> None:
    """Тестирует логирование ошибки в файл"""
    filename: Path = tmp_path / "test_log.txt"

    @log(filename=str(filename))
    def test_func(x: int, y: int) -> None:
        raise TypeError("Custom error")

    with pytest.raises(TypeError, match="Custom error"):
        test_func(10, y=5)

    content: str = filename.read_text()
    assert "test_func error: TypeError. Inputs: (10,), {'y': 5}\n" in content


def test_log_preserves_metadata() -> None:
    """Проверяет сохранение метаданных исходной функции"""

    @log()
    def original_func() -> int:
        """Тестовая документация"""
        return 42

    assert original_func.__name__ == "original_func"
    assert original_func.__doc__ == "Тестовая документация"
