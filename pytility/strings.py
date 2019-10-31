# -*- coding: utf-8 -*-

"""String utilities."""

import string as string_lib

from typing import Any, Optional

PRINTABLE_SET = frozenset(string_lib.printable)
NON_PRINTABLE_SET = frozenset(chr(i) for i in range(128)) - PRINTABLE_SET
NON_PRINTABLE_TANSLATE = {ord(character): None for character in NON_PRINTABLE_SET}


def to_str(string: Any, encoding: str = "utf-8") -> Optional[str]:
    """Safely returns either string or None."""

    string = (
        string
        if isinstance(string, str)
        else string.decode(encoding)
        if isinstance(string, bytes)
        else None
    )

    return string.translate(NON_PRINTABLE_TANSLATE) if string is not None else None


def normalize_space(item: Any, preserve_newline: bool = False) -> str:
    """Normalize space in a string."""

    item = to_str(item)

    if not item:
        return ""

    if preserve_newline:
        try:
            return "\n".join(
                normalize_space(line) for line in item.splitlines()
            ).strip()
        except Exception:
            return ""

    try:
        return " ".join(item.split())
    except Exception:
        return ""
