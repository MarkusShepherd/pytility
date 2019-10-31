# -*- coding: utf-8 -*-

"""Parsers."""

from datetime import datetime, timezone
from typing import Any, Optional

import dateutil.parser


def parse_int(string: Any, base: int = 10) -> Optional[int]:
    """Safely convert an object to int if possible, else return None."""

    if isinstance(string, int):
        return string

    try:
        return int(string, base=base)
    except Exception:
        pass

    try:
        return int(string)
    except Exception:
        pass

    return None


def parse_float(number: Any) -> Optional[float]:
    """Safely convert an object to float if possible, else return None."""

    try:
        return float(number)
    except Exception:
        pass
    return None


def parse_bool(item: Any) -> bool:
    """Parses an item and converts it to a boolean."""

    if isinstance(item, int):
        return bool(item)
    if item in ("True", "true", "Yes", "yes"):
        return True
    integer = parse_int(item)
    if integer is not None:
        return bool(integer)
    return False


def _add_tz(
    date: Optional[datetime], tzinfo: Optional[timezone] = None
) -> Optional[datetime]:
    return (
        date if not tzinfo or not date or date.tzinfo else date.replace(tzinfo=tzinfo)
    )


def parse_date(
    date: Any, tzinfo: Optional[timezone] = None, format_str: Optional[str] = None
) -> Optional[datetime]:
    """Try to turn input into a datetime object."""

    if not date:
        return None

    # already a datetime
    if isinstance(date, datetime):
        return _add_tz(date, tzinfo)

    # parse as epoch time
    timestamp = parse_float(date)
    if timestamp is not None:
        return datetime.fromtimestamp(timestamp, tzinfo or timezone.utc)

    if format_str:
        try:
            # parse as string in given format
            return _add_tz(datetime.strptime(date, format_str), tzinfo)
        except Exception:
            pass

    try:
        # parse as string
        return _add_tz(dateutil.parser.parse(date), tzinfo)
    except Exception:
        pass

    try:
        # parse as (year, month, day, hour, minute, second, microsecond, tzinfo)
        return datetime(*date)
    except Exception:
        pass

    try:
        # parse as time.struct_time
        return datetime(*date[:6], tzinfo=tzinfo or timezone.utc)
    except Exception:
        pass

    return None
