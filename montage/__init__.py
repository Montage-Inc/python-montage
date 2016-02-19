__author__ = 'Derek Payton <dpayton@mntge.com>'
__copyright__ = 'Copyright (c) Montage, Inc'
__description__ = 'Python bindings for Montage'
__version__ = '2.0.0'
__license__ = 'MIT License'

from .client import Client, client
from .errors import MontageError, HttpError
from .query import Query
from .scripting import Script, RunLua
