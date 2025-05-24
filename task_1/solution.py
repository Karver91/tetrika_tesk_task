from itertools import zip_longest


def strict(func):
    def inner(*args, **kwargs):
        annotations = func.__annotations__
        if annotations.get("return") is not None:
            del annotations["return"]
        if args:
            kwargs = dict(zip_longest(annotations.keys(), args))
        if len(kwargs) != len(annotations):
            raise TypeError(f"{func.__name__}() принимает {len(annotations)} аргументов, но {len(kwargs)} были переданы")

        for param_name, value in kwargs.items():
            if param_name not in annotations.keys():
                raise KeyError(f"Ключ {param_name!r} не найден в параметрах функции {func.__name__}()")
            if not isinstance(value, annotations[param_name]):
                raise TypeError(
                    f"Аргумент {param_name!r} должен быть {annotations[param_name].__name__!r}, "
                    f"получен {type(kwargs[param_name]).__name__!r}")
        return func(**kwargs)
    return inner


@strict
def sum_two(a: int, b: int) -> int:
    return a + b
