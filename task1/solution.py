import inspect


def strict(func):
    sig = inspect.signature(func)
    expected_types = func.__annotations__

    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        for name, value in bound_args.arguments.items():
            if name in expected_types:
                expected = expected_types[name]
                if not isinstance(value, expected):
                    raise TypeError(
                        f"Argument '{name}' must be of type {expected.__name__}, got {type(value).__name__}"
                    )

        result = func(*args, **kwargs)

        if 'return' in expected_types:
            expected_return_type = expected_types['return']
            if not isinstance(result, expected_return_type):
                raise TypeError(
                    f"Return value must be of type {expected_return_type.__name__}, got {type(result).__name__}"
                )

        return result

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b

print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
