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
    def __init__(self, client=None):
        self.client = client
        self.session = self.make_session()

    def make_session(self):
        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        session = requests.Session()
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update({
            'Accept': 'application/json',
            'User-Agent': USER_AGENT,
        })
        return session

    def get_headers(self, **kwargs):
        headers = {}
        if self.client.token:
            headers['Authorization'] = 'Token {0}'.format(self.client.token)
        headers.update(kwargs)
        return headers

    def is_json(self, response):
        return response.headers['Content-Type'] == 'application/json'

    def decode(self, content):
        return JSONDecoder().decode(content.decode('utf-8'))

    def encode(self, obj):
        return JSONEncoder().encode(obj)

    def request(self, url, method=None, **kwargs):
        response = self.get_response(url, method, **kwargs)

        # Non-2xx responses get a generic HttpError. If we need to
        # differentiate between 400's and 500's, we can do that at
        # a later date.
        if not (200 <= response.status_code <= 299):
            if self.is_json(response):
                data = self.decode(response.content)
                raise HttpError(data['errors'][0]['detail'], response)
            raise HttpError(response.text, response)

        # Success! Return the response content as JSON or text as needed.
        if self.is_json(response):
            value = self.decode(response.content)
        else:
            value = response.text
        del response
        return value

    def get_response(self, url, method=None, **kwargs):
        method = method or 'get'
        headers = self.get_headers(**kwargs.pop('headers', {}))

        data = kwargs.pop('json', None)
        if data is not None:
            kwargs['data'] = self.encode(data)
            headers['Content-Type'] = 'application/json'

        return self.session.request(method, url, headers=headers, **kwargs)

    def get(self, url, **kwargs):
        return self.request(url, method='get', **kwargs)

    def post(self, url, **kwargs):
        return self.request(url, method='post', **kwargs)

    def put(self, url, **kwargs):
        return self.request(url, method='put', **kwargs)

    def patch(self, url, **kwargs):
        return self.request(url, method='patch', **kwargs)
