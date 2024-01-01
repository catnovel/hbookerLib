import json
import warnings
import functools


def deprecated(reason):
    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated and will be removed in a future version. {reason}",
                category=DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)

        return new_func

    return decorator


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True
