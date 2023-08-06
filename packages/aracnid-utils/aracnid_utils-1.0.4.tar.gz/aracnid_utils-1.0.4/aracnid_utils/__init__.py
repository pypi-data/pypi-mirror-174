"""This package contains utilities that I use frequently.
"""
from importlib.metadata import version

from aracnid_utils.datetime_utils import timespan, isoweek, fromisoweek, EST


__version__ = version(__package__)
