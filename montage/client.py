import mimetypes
import os

from cached_property import cached_property

from .compat import urljoin
from .requestor import APIRequestor

BASE_URL = 'mntge.com'


class UsersAPI(object):
    def __init__(self, client):
        self.client = client

    def authenticate(self, email, password):
        response = self.client.request('auth', 'post', data={
            'username': email,
            'password': password
        })
        self.client.token = response.get('data', {}).get('token')
        if self.client.token is None:
            return False
        return True

    def info(self):
        return self.client.request('auth/user')


class SchemasAPI(object):
    def __init__(self, client):
        self.client = client

    def all(self):
        return self.client.request('schemas')

    def get(self, schema_id):
        return self.client.request('schemas/{0}'.format(schema_id))


class FilesAPI(object):
    def __init__(self, client):
        self.client = client

    def all(self):
        return self.client.request('files')

    def get(self, file_id):
        return self.client.request('files/{0}'.format(file_id))

    def delete(self, file_id):
        return self.client.request('files/{0}'.format(file_id), 'delete')

    def save(self, *files):
        '''
            Each file is extected to be a tuple of (name, content), where
            content is a file-like object or the contents as a string.

            client.files.save(('foo.txt', open('/path/to/foo.txt')))
            client.files.save(('foo.txt', StringIO('This is foo.txt')))
            client.files.save(('foo.txt', 'This is foo.txt'))
        '''
        file_list = []
        for name, contents in files:
            content_type = mimetypes.guess_type(name)[0]
            file_list.append(('file', (name, contents, content_type)))
        return self.client.request('files', 'post', files=file_list)


class DataAPI(object):
    def __init__(self, client):
        self.client = client

    def query(self, query):
        # TODO
        pass


class Client(object):
    def __init__(self, subdomain, token=None, api_version=1, url=BASE_URL):
        self.domain = '{0}.{1}'.format(subdomain, url)
        self.token = token
        self.api_version = api_version
        self.url = url

    def request(self, endpoint, method=None, **kwargs):
        requestor = APIRequestor(self.token)
        return requestor.request(self.url(endpoint), method, **kwargs)

    def url(self, endpoint):
        path = '/api/v{0}/{1}/'.format(self.api_version, endpoint)
        return 'https://{0}{1}'.format(self.domain, path)

    @cached_property
    def user(self):
        return UsersAPI(self)

    @cached_property
    def schemas(self):
        return SchemasAPI(self)

    @cached_property
    def files(self):
        return FilesAPI(self)

    @cached_property
    def data(self):
        return DataAPI(self)


client = Client(
    subdomain=os.environ.get('MONTAGE_SUBDOMAIN'),
    token=os.environ.get('MONTAGE_TOKEN')
)
