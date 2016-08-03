import datetime
import decimal
import uuid

import pytest

from montage.encoders import (
    PyJSONDecoder, PyJSONEncoder,
    RapidJSONDecoder, RapidJSONEncoder,
    JSONEncoder, JSONDecoder
)

from .utils import MontageTests

try:
    import rapidjson
except ImportError:
    rapidjson = False


class PyJSONTests(MontageTests):
    JSON_ENCODER = PyJSONEncoder

    def setUp(self):
        self.encoder = self.JSON_ENCODER()
        super(PyJSONTests, self).setUp()

    def test_datetime(self):
        dt = datetime.datetime(2004, 12, 20, 10, 45)
        encoded = self.encoder.encode(dt)
        expected = '"2004-12-20T10:45:00"'
        assert encoded == expected

    def test_date(self):
        dt = datetime.date(2005, 4, 13)
        encoded = self.encoder.encode(dt)
        expected = '"2005-04-13"'
        assert encoded == expected

    def test_time(self):
        dt = datetime.time(16, 20)
        encoded = self.encoder.encode(dt)
        expected = '"16:20:00"'
        assert encoded == expected

    def test_uuid(self):
        id = uuid.UUID('92b36f8a-f4e4-43f1-804e-11b2e34b27c3')
        encoded = self.encoder.encode(id)
        expected = '"92b36f8a-f4e4-43f1-804e-11b2e34b27c3"'
        assert encoded == expected

    def test_decimal(self):
        d = decimal.Decimal('3.14159')
        encoded = self.encoder.encode(d)
        expected = '"3.14159"'
        assert encoded == expected


@pytest.mark.skipif(rapidjson is False, reason='Requires python-rapidjson')
class RapidJSONTests(PyJSONTests):
    JSON_ENCODER = RapidJSONEncoder

    def test_rapidjson_installed(self):
        assert JSONDecoder == RapidJSONDecoder
        assert JSONEncoder == RapidJSONEncoder
