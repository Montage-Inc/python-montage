import mimetypes
import os

from cached_property import cached_property

from .api import DataAPI, FileAPI, SchemaAPI
from .compat import urljoin
from .requestor import APIRequestor

BASE_URL = 'mntge.com'


class Client(object):
    def __init__(self, subdomain, token=None, url=BASE_URL):
        self.domain = '{0}.{1}'.format(subdomain, url)
        self.token = token

    def request(self, endpoint, method=None, **kwargs):
        requestor = APIRequestor(self.token)
        return requestor.request(self.url(endpoint), method, **kwargs)

    def url(self, endpoint):
        return 'https://{domain}/api/v1/{endpoint}/'.format(self.domain, endpoint)

    def authenticate(self, email, password):
        response = self.request('auth', 'post', data={
            'username': email,
            'password': password
        })
        self.token = response.get('data', {}).get('token')
        if self.token is None:
            return False
        return True

    def user(self):
        return self.request('auth/user')

    @cached_property
    def schemas(self):
        return SchemaAPI(self)

    @cached_property
    def files(self):
        return FileAPI(self)

    @cached_property
    def data(self):
        return DataAPI(self)


client = Client(
    subdomain=os.environ.get('MONTAGE_SUBDOMAIN'),
    token=os.environ.get('MONTAGE_TOKEN')
)
