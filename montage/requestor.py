import json
import platform
import requests

from . import __version__
from .compat import urljoin
from .encoder import SmartJSONEncoder

__all__ = ('APIRequestor',)

# This dictionary is used to dynamically select the appropriate platform for
# the user agent string.
OS_VERSION_INFO = {
    'Linux': '%s' % (platform.linux_distribution()[0]),
    'Windows': '%s' % (platform.win32_ver()[0]),
    'Darwin': '%s' % (platform.mac_ver()[0]),
}

USER_AGENT = 'python-montage/{lib_ver} {py_impl}/{py_ver} {os}/{os_dist}'.format(
    lib_ver=__version__,
    py_impl=platform.python_implementation(),
    py_ver=platform.python_version(),
    os=platform.system(),
    os_dist=OS_VERSION_INFO.get(platform.system(), 'X')
)


class APIRequestor(object):
    def __init__(self, token=None):
        self.token = token

    def get_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': USER_AGENT,
        }

        if self.token:
            headers['Authorization'] = 'Token {0}'.format(self.token)

        return headers

    def request(self, url, method=None, **kwargs):
        method = method or 'get'

        headers = self.get_headers()
        headers.update(kwargs.pop('headers', {}))

        data = kwargs.pop('json', None)
        if data:
            kwargs['data'] = json.dumps(data, cls=SmartJSONEncoder)

        kwargs.setdefault('timeout', 10)

        response = requests.request(method, url, headers=headers, **kwargs)

        # if response.status_code != 200:
        #     raise HttpError(response.status_code, response)

        return response.json()

    def get(self, url, **kwargs):
        return self.request(url, method='get', **kwargs)

    def post(self, url, **kwargs):
        return self.request(url, method='post', **kwargs)
