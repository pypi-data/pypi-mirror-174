import typing

from panther_sdk import detection, PantherEvent

__all__ = ["deep_equal", "deep_equal_pattern", "deep_in"]


def deep_exists(path: str) -> detection.PythonFilter:
    """Returns True when a value at the provided path exists"""

    def _deep_exists(event: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            event,
        )

        return bool(actual is not None)

    return detection.PythonFilter(func=_deep_exists)


def deep_not_exists(path: str) -> detection.PythonFilter:
    """Returns True when a value at the provided path does not exist"""

    def _deep_not_exists(event: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            event,
        )

        return bool(actual is None)

    return detection.PythonFilter(func=_deep_not_exists)


def deep_equal(path: str, value: typing.Any) -> detection.PythonFilter:
    """Returns True when the provided value equals the value at the provided path"""

    def _deep_equal(event: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            event,
        )

        return bool(actual == value)

    return detection.PythonFilter(func=_deep_equal)


def deep_not_equal(path: str, value: typing.Any) -> detection.PythonFilter:
    """Returns True when the provided value does not equal the value at the provided path"""

    def _deep_not_equal(event: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            event,
        )

        return bool(actual != value)

    return detection.PythonFilter(func=_deep_not_equal)


def deep_equal_pattern(path: str, pattern: str) -> detection.PythonFilter:
    """Returns True when the provided pattern matches the value at the provided path using the 're' module"""

    def _deep_equal_pattern(evt: PantherEvent) -> bool:
        import re
        import functools
        import collections

        keys = path.split(".")
        regex = re.compile(pattern)

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            evt,
        )

        return bool(regex.search(actual))

    return detection.PythonFilter(func=_deep_equal_pattern)


def deep_not_equal_pattern(path: str, pattern: str) -> detection.PythonFilter:
    """Returns True when the provided pattern does not match the value at the provided path using the 're' module"""

    def _deep_not_equal_pattern(evt: PantherEvent) -> bool:
        import re
        import functools
        import collections

        keys = path.split(".")
        regex = re.compile(pattern)

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            evt,
        )

        return not bool(regex.search(actual))

    return detection.PythonFilter(func=_deep_not_equal_pattern)


def deep_in(path: str, value: typing.List[typing.Any]) -> detection.PythonFilter:
    """Returns True when one of the provided values are equal to the value at the provided path"""

    def _deep_in(evt: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            evt,
        )

        return actual in value

    return detection.PythonFilter(
        func=_deep_in,
    )


def deep_not_in(path: str, value: typing.List[typing.Any]) -> detection.PythonFilter:
    """Returns True when none of the provided values are equal to the value at the provided path"""

    def _deep_not_in(evt: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            evt,
        )

        return actual not in value

    return detection.PythonFilter(
        func=_deep_not_in,
    )


def deep_less_than(
    path: str, value: typing.Union[int, float]
) -> detection.PythonFilter:
    """Returns True if the value at the provided path is less than a value"""

    def _deep_less_than(evt: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            evt,
        )

        return bool(actual < value)

    return detection.PythonFilter(
        func=_deep_less_than,
    )


def deep_less_than_or_equal(
    path: str, value: typing.Union[int, float]
) -> detection.PythonFilter:
    """Returns True if the value at the provided path is less than or equal to a value"""

    def _deep_less_than_or_equal(evt: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            evt,
        )

        return bool(actual <= value)

    return detection.PythonFilter(
        func=_deep_less_than_or_equal,
    )


def deep_greater_than(
    path: str, value: typing.Union[int, float]
) -> detection.PythonFilter:
    """Returns True if the value at the provided path is greater than a value"""

    def _deep_greater_than(evt: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            evt,
        )

        return bool(actual > value)

    return detection.PythonFilter(
        func=_deep_greater_than,
    )


def deep_greater_than_or_equal(
    path: str, value: typing.Union[int, float]
) -> detection.PythonFilter:
    """Returns True if the value at the provided path is greater than or equal to a value"""

    def _deep_greater_than_or_equal(evt: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            evt,
        )

        return bool(actual >= value)

    return detection.PythonFilter(
        func=_deep_greater_than_or_equal,
    )


def deep_between(
    path: str,
    val_min: typing.Union[int, float],
    val_max: typing.Union[int, float],
) -> detection.PythonFilter:
    """Returns True if the value at the provided path is between (or equal to) a maximum and minimum"""

    if val_min >= val_max:
        raise RuntimeError("deep_between: min must be greater than max")

    def _deep_between(evt: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            evt,
        )

        return bool(val_min <= actual <= val_max)

    return detection.PythonFilter(
        func=_deep_between,
    )


def deep_between_exclusive(
    path: str,
    val_min: typing.Union[int, float],
    val_max: typing.Union[int, float],
) -> detection.PythonFilter:
    """Returns True if the value at the provided path is between, but not equal to, a maximum and minimum"""

    if val_min >= val_max:
        raise RuntimeError("deep_between_exclusive: min must be greater than max")

    def _deep_between_exclusive(evt: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.abc.Mapping)
            else None,
            keys,
            evt,
        )

        return bool(val_min < actual < val_max)

    return detection.PythonFilter(
        func=_deep_between_exclusive,
    )
