"""Beautiful and helpful exceptions

Just set your `BETTER_EXCEPTIONS` environment variable. It handles the rest.


   Name: better_exceptions
 Author: Josh Junon
  Email: josh@junon.me
    URL: github.com/qix-/better-exceptions
License: Copyright (c) 2017 Josh Junon, licensed under the MIT license
"""

from __future__ import absolute_import, print_function

import logging
import sys

from .color import SHOULD_ENCODE, STREAM, SUPPORTS_COLOR, to_byte
from .context import PY3
from .formatter import CAP_CHAR, MAX_LENGTH, PIPE_CHAR, THEME, ExceptionFormatter
from .log import BetExcLogger
from .log import patch as patch_logging
from .repl import get_repl, interact

__version__ = "0.3.3"


THEME = THEME.copy()  # Users customizing the theme should not impact core


def write_stream(data, stream=STREAM):
    if SHOULD_ENCODE:
        data = to_byte(data)

        if PY3:
            stream.buffer.write(data)
        else:
            stream.write(data)
    else:
        stream.write(data)


def format_exception(exc, value, tb):
    formatter = ExceptionFormatter(
        colored=SUPPORTS_COLOR,
        theme=THEME,
        max_length=MAX_LENGTH,
        pipe_char=PIPE_CHAR,
        cap_char=CAP_CHAR,
    )
    return list(formatter.format_exception(exc, value, tb))


def excepthook(exc, value, tb):
    formatted = "".join(format_exception(exc, value, tb))
    write_stream(formatted, STREAM)


def hook():
    sys.excepthook = excepthook

    logging.setLoggerClass(BetExcLogger)
    patch_logging()

    if hasattr(sys, "ps1"):
        print(
            "WARNING: better_exceptions will only inspect code from the command line\n"
            "         when using: `python -m better_exceptions'. Otherwise, only code\n"
            "         loaded from files will be inspected!",
            file=sys.stderr,
        )
