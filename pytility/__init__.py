# -*- coding: utf-8 -*-

"""Initialisations."""

from .__version__ import VERSION, __version__
from .files import concat_files
from .iterables import arg_to_iter, batchify, clear_list, take_first, window
from .parsers import parse_bool, parse_date, parse_float, parse_int
from .strings import normalize_space, to_str
