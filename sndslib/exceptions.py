#!/usr/bin/env python3
# sndslib by @undersfx

import sys


class SndsHttpError(Exception):
    "Raise when http request for SNDS api raises a error"
    def __init__(self, error) -> None:
        super().__init__(error)
        print(f'Could not connect to SNDS API. Reason: {error}')


class SndsCliError(Exception):
    "Raise when sndslib cli raises a error"
    def __init__(self, error) -> None:
        sys.exit(1)
