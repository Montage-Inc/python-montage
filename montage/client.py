import mimetypes
import os

from cached_property import cached_property

from .api import DocumentsAPI, FileAPI, SchemaAPI, UserAPI
from .compat import urljoin
from .requestor import APIRequestor

__all__ = ('Client', 'client')

BASE_URL = 'mntge.com'


class Client(object):
    def __init__(self, subdomain, token=None, url=BASE_URL):
        self.domain = '{0}.{1}'.format(subdomain, url)
        self.token = token

    def request(self, endpoint, method=None, **kwargs):
        requestor = APIRequestor(self.token)
        return requestor.request(self.url(endpoint), method, **kwargs)

    def url(self, endpoint):
        return 'https://{domain}/api/v1/{endpoint}/'.format(
            domain=self.domain,
            endpoint=endpoint
        )

    def authenticate(self, email, password):
        response = self.request('user', method='post', data={
            'username': email,
            'password': password
        })
        self.token = response.get('data', {}).get('token')
        if self.token is None:
            return False
        return True

    def user(self):
        if self.token:
            return self.request('user')

    def run(self, **kwargs):
        queryset = {key: thing.as_dict() for key, thing in kwargs.items()}
        return self.client.request('query', method='post', json=queryset)

    @cached_property
    def documents(self):
        return DocumentsAPI(self)

    @cached_property
    def files(self):
        return FileAPI(self)

    @cached_property
    def schemas(self):
        return SchemaAPI(self)

    @cached_property
    def users(self):
        return UserAPI(self)


client = Client(
    subdomain=os.environ.get('MONTAGE_SUBDOMAIN'),
    token=os.environ.get('MONTAGE_TOKEN')
)
