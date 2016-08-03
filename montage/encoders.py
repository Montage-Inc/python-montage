import datetime
import decimal
import json
import uuid

try:
    import rapidjson
except ImportError:
    rapidjson = False

__all__ = ('JSONDecoder', 'JSONEncoder')


def is_aware(value):
    """
    Determines if a given datetime.datetime is aware.
    The logic is described in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    return value.tzinfo is not None and \
        value.tzinfo.utcoffset(value) is not None



class PyJSONDecoder(json.JSONDecoder):
    pass


class PyJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder that knows how to encode date/times, Decimals, and UUIDs.
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r

        if isinstance(o, datetime.date):
            return o.isoformat()

        if isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r

        if isinstance(o, decimal.Decimal):
            return str(o)

        if isinstance(o, uuid.UUID):
            return str(o)

        return super(SmartJSONEncoder, self).default(o)


class RapidJSONDecoder(object):
    def decode(self, data):
        return rapidjson.loads(data, use_decimal=True)


class RapidJSONEncoder(object):
    def __init__(self):
        self._encoder = PyJSONEncoder()

    def encode(self, data):
        return rapidjson.dumps(data, default=self._encoder.default)


if rapidjson is False:
    JSONDecoder = PyJSONDecoder
    JSONEncoder = PyJSONEncoder
else:
    JSONDecoder = RapidJSONDecoder
    JSONEncoder = RapidJSONEncoder
