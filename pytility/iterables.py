# -*- coding: utf-8 -*-

"""Iterable utilities."""

from collections import OrderedDict
from itertools import groupby
from typing import Any, Iterable, List, Optional, TypeVar

ITERABLE_SINGLE_VALUES = (dict, str, bytes)
TYPE = TypeVar("TYPE")


def clear_list(items: Iterable[Optional[TYPE]]) -> List[TYPE]:
    """Return unique items in order of first ocurrence."""
    return list(OrderedDict.fromkeys(filter(None, items)))


def arg_to_iter(arg: Any) -> Iterable:
    """Wraps arg into tuple if not an iterable."""

    if arg is None:
        return ()

    if not isinstance(arg, ITERABLE_SINGLE_VALUES) and hasattr(arg, "__iter__"):
        return arg

    return (arg,)


def take_first(items):
    """Take first item that is not None or zero-length str."""

    for item in arg_to_iter(items):
        if item is not None and item != "":
            return item

    return None


def batchify(iterable, size):
    """Make batches of given size."""
    for _, group in groupby(enumerate(iterable), key=lambda x: x[0] // size):
        yield (x[1] for x in group)
