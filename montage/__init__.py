__author__ = 'Derek Payton <dpayton@mntge.com>'
__copyright__ = 'Copyright (c) Montage, Inc'
__description__ = 'Python bindings for Montage'
__version__ = '2.0.0'
__license__ = 'MIT License'

from . import geospatial
from .client import Client, client
from .command import Command
from .errors import MontageError, HttpError, ValidationError
from .query import Field, Query
