#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2021 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pycursorsio project, which is MIT-licensed.
# *****************************************************************************
"""Python client for cursors.io, using pygame and websockets."""

from .cli import cli

if __name__ == '__main__':
    cli()
