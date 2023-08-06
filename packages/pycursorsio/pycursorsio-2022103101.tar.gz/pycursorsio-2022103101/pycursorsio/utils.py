#!/usr/bin/env python3
# ****************************************************************************
# Copyright (C) 2022 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pycursorsio project, which is MIT-licensed.
# ****************************************************************************
"""Utilities."""

import string
from logging import Logger

__all__ = ['log_data']

printable_bytes = (
    string.ascii_letters + string.digits + string.punctuation
).encode('ascii')


def get_readable_bytes(data: bytes) -> str:
    """Get readable bytes."""
    return b''.join(
        bytes((c,)) if c in printable_bytes else b'.'
        for c in data
    ).decode()


def log_data(logger: Logger, data: bytes) -> None:
    """Log data."""
    left = len(data) % 8
    for offset in range(0, len(data) - left, 8):
        extract = data[offset:offset + 8]
        logger.debug(
            '  |%-8s|  %02X %02X %02X %02X %02X %02X %02X %02X',
            get_readable_bytes(extract),
            *extract,
        )

    if left:
        extract = data[-left:]

        logger.debug(
            '  |%-8s| ' + ' %02X' * len(extract),
            get_readable_bytes(extract),
            *extract,
        )
