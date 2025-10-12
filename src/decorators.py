from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для логирования выполнения функций.

    Args:
        filename: Имя файла для записи логов. Если None, логи выводятся в консоль.

    Returns:
        Декоратор функции, который добавляет логирование.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            try:
                result = func(*args, **kwargs)
                success_info = f"{func.__name__} ok\n"

                if filename:
                    with open(filename, "a") as f:
                        f.write(success_info)
                else:
                    print(success_info, end="")

                return result

            except Exception as e:
                error_info = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"

                if filename:
                    with open(filename, "a") as f:
                        f.write(error_info)
                else:
                    print(error_info, end="")

        return wrapper

    return decorator
