# -*- coding: utf-8 -*-

"""File utilities."""

import logging
import os
import shutil

from typing import Iterable, TextIO, Union

LOGGER = logging.getLogger(__name__)

FilePath = Union[str, bytes, os.PathLike, TextIO]


def _copy_file(src: FilePath, dst: TextIO, ensure_newline: bool) -> int:
    if isinstance(src, (str, bytes, os.PathLike)):
        LOGGER.debug("copy data from <%s>", src)
        with open(src, "r") as in_file:
            return _copy_file(in_file, dst, ensure_newline)

    shutil.copyfileobj(src, dst)

    if not src.tell():
        return 0

    copied = src.tell()

    if ensure_newline:
        src.seek(src.tell() - 1)

        if src.read(1) != "\n":
            dst.write("\n")
            copied += 1

    return copied


def concat_files(
    dst: FilePath, srcs: Iterable[FilePath], ensure_newline: bool = False
) -> int:
    """Concatenate files, returning the total number of bytes copied."""

    if isinstance(dst, (str, bytes, os.PathLike)):
        LOGGER.info("concatenating files into <%s>", dst)
        with open(dst, "w") as out_file:
            return concat_files(out_file, srcs, ensure_newline)

    total = 0

    for src in srcs:
        total += _copy_file(src, dst, ensure_newline)

    LOGGER.info("done concatenating, %d bytes in total", total)

    return total
