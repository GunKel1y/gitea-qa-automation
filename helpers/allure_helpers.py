import inspect
from collections.abc import Collection
from functools import wraps

from allure_commons._allure import StepContext


_HIDDEN_ARGS = ("self", "cls")


def step(title: str, *, mask: Collection[str] = ()):
    """@allure.step для методов страниц и компонентов

    title: текст шага. Можно подставлять аргументы {имя} и атрибуты объекта {self.имя}
    mask:  имена аргументов, значения которых в отчёте заменяются на *** (в шаге также)
    """

    def decorator(func):
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            shows = {
                name: ("***" if name in mask else value)
                for name, value in bound.arguments.items()
                if name not in _HIDDEN_ARGS
            }
            namespace = {**bound.arguments, **shows}

            with StepContext(title.format(**namespace), shows):
                return func(*args, **kwargs)

        return wrapper

    return decorator
