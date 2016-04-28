import mimetypes
import os

from cached_property import cached_property

from . import api
from .compat import urljoin
from .requestor import APIRequestor

__all__ = ('Client', 'client')


class Client(object):
    domain = 'mntge.com'
    protocol = 'https'

    def __init__(self, subdomain, token=None):
        self.subdomain = subdomain
        self.token = token

    def request(self, endpoint, method=None, **kwargs):
        requestor = APIRequestor(self.token)
        return requestor.request(self.url(endpoint), method, **kwargs)

    def url(self, endpoint):
        return '{protocol}://{subdomain}.{domain}/api/v1/{endpoint}/'.format(
            protocol=self.protocol,
            subdomain=self.subdomain,
            domain=self.domain,
            endpoint=endpoint,
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

    def execute(self, **kwargs):
        queryset = {key: executable.as_dict()
            for key, executable in kwargs.items()}
        return self.request('execute', method='post', json=queryset)

    @cached_property
    def documents(self):
        return api.DocumentsAPI(self)

    @cached_property
    def files(self):
        return api.FileAPI(self)

    @cached_property
    def roles(self):
        return api.RoleAPI(self)

    @cached_property
    def schemas(self):
        return api.SchemaAPI(self)

    @cached_property
    def users(self):
        return api.UserAPI(self)

    @cached_property
    def policy(self):
        return api.PolicyAPI(self)


client = Client(
    subdomain=os.environ.get('MONTAGE_SUBDOMAIN'),
    token=os.environ.get('MONTAGE_TOKEN')
)
