import platform
import requests

from . import __version__
from .compat import urljoin
from .encoders import JSONDecoder, JSONEncoder
from .errors import HttpError

__all__ = ('APIRequestor',)

USER_AGENT = 'python-montage/{lib_ver} {py_impl}/{py_ver} {os}/{os_dist}'.format(
    lib_ver=__version__,
    py_impl=platform.python_implementation(),
    py_ver=platform.python_version(),
    os=platform.system(),
    os_dist={
        'Linux': lambda: platform.linux_distribution()[0],
        'Windows': lambda: platform.win32_ver()[0],
        'Darwin': lambda: platform.mac_ver()[0],
        'Java': lambda: platform.java_ver()[0],
    }.get(platform.system(), lambda: '-')()
)


class APIRequestor(object):
    def __init__(self, token=None):
        self.token = token

    def get_headers(self):
        headers = {
            'Accept': 'application/json',
            'User-Agent': USER_AGENT,
        }

        if self.token:
            headers['Authorization'] = 'Token {0}'.format(self.token)

        return headers

    def is_json(self, response):
        return response.headers['Content-Type'] == 'application/json'

    def decode(self, content):
        return JSONDecoder().decode(content.decode('utf-8'))

    def encode(self, obj):
        return JSONEncoder().encode(obj)

    def request(self, url, method=None, **kwargs):
        method = method or 'get'

        headers = self.get_headers()
        headers.update(kwargs.pop('headers', {}))

        data = kwargs.pop('json', None)
        if data:
            kwargs['data'] = self.encode(data)
            headers['Content-Type'] = 'application/json'

        kwargs.setdefault('timeout', 10)

        response = requests.request(method, url, headers=headers, **kwargs)

        # Non-2xx responses get a generic HttpError. If we need to
        # differentiate between 400's and 500's, we can do that at
        # a later date.
        if not (200 <= response.status_code <= 299):
            if self.is_json(response):
                data = self.decode(response.content)
                raise HttpError(response.status_code, data['errors'][0]['detail'])
            raise HttpError(response.status_code, response.text)

        # Success! Return the response content as JSON or text as needed.
        if self.is_json(response):
            return self.decode(response.content)
        return response.text

    def get(self, url, **kwargs):
        return self.request(url, method='get', **kwargs)

    def post(self, url, **kwargs):
        return self.request(url, method='post', **kwargs)

    def put(self, url, **kwargs):
        return self.request(url, method='put', **kwargs)

    def patch(self, url, **kwargs):
        return self.request(url, method='patch', **kwargs)
