# -*- coding: utf-8 -*-

"""Iterable utilities."""

from collections import OrderedDict, abc
from itertools import groupby, tee
from typing import Any, Generator, Iterable, List, Optional, Tuple, TypeVar

ITERABLE_SINGLE_VALUES = (dict, str, bytes)
Typed = TypeVar("Typed")


def clear_list(items: Iterable[Optional[Typed]]) -> List[Typed]:
    """Return unique items in order of first ocurrence."""
    return list(OrderedDict.fromkeys(filter(None, items)))


def arg_to_iter(arg: Any) -> Iterable[Any]:
    """Wraps arg into tuple if not an iterable."""

    if arg is None:
        return ()

    if isinstance(arg, abc.Iterable) and not isinstance(arg, ITERABLE_SINGLE_VALUES):
        return arg

    return (arg,)


def take_first(items: Any) -> Any:
    """Take first item that is not None or zero-length str."""

    for item in arg_to_iter(items):
        if item is not None and item != "":
            return item

    return None


def batchify(
    iterable: Iterable[Typed], size: int
) -> Generator[Iterable[Typed], None, None]:
    """Make batches of given size."""
    for _, group in groupby(enumerate(iterable), key=lambda x: x[0] // size):
        yield (x[1] for x in group)


def window(iterable: Iterable[Typed], size: int = 2) -> Iterable[Tuple[Typed, ...]]:
    """Sliding window of an iterator."""

    iterables = tee(iterable, size)

    for num, itb in enumerate(iterables):
        for _ in range(num):
            next(itb, None)

    return zip(*iterables)
