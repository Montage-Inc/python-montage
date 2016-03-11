import json
import os
import responses
from .utils import MontageTests, make_response, DOCUMENTS, FILES, SCHEMAS, USER

try:
    from cStringIO import StringIO
except ImportError:
    # Importing BytesIO as StringIO feels wrong...
    from io import BytesIO as StringIO


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class DocumentsAPITests(MontageTests):
    @responses.activate
    def test_get_document(self):
        doc = DOCUMENTS[0]
        endpoint = 'https://testco.hexxie.com/api/v1/schemas/{0}/documents/{1}/'.format('movies', doc['id'])
        responses.add(responses.GET, endpoint, body=make_response(doc),
            content_type='application/json')

        response = self.client.documents.get('movies', doc['id'])
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_delete_document(self):
        doc = DOCUMENTS[0]
        endpoint = 'https://testco.hexxie.com/api/v1/schemas/{0}/documents/{1}/'.format('movies', doc['id'])
        responses.add(responses.DELETE, endpoint, status=204)

        response = self.client.documents.remove('movies', doc['id'])
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint


class FileAPITests(MontageTests):
    @responses.activate
    def test_file_list(self):
        endpoint = 'https://testco.hexxie.com/api/v1/files/'
        responses.add(responses.GET, endpoint, body=make_response(FILES),
            content_type='application/json')

        response = self.client.files.list()
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_file_filter(self):
        endpoint = 'https://testco.hexxie.com/api/v1/files/'
        responses.add(responses.GET, endpoint, body=make_response(FILES),
            content_type='application/json')

        gigabyte = 1024 * 1024 * 1024
        response = self.client.files.list(size__gte=gigabyte)
        assert len(responses.calls) == 1
        query = urlparse(responses.calls[0].request.url).query
        assert query == 'size__gte={0}'.format(gigabyte)

    @responses.activate
    def test_file(self):
        file = FILES[0]
        endpoint = 'https://testco.hexxie.com/api/v1/files/{0}/'.format(file['id'])
        responses.add(responses.GET, endpoint, body=make_response(file),
            content_type='application/json')

        response = self.client.files.get(file['id'])
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_file_upload(self):
        endpoint = 'https://testco.hexxie.com/api/v1/files/'
        responses.add(responses.POST, endpoint, body=make_response([FILES[0]]),
            content_type='application/json')

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/python-powered.png')
        response = self.client.files.save(('python-powered.png', open(path, 'rb')))
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_file_upload_multiple(self):
        endpoint = 'https://testco.hexxie.com/api/v1/files/'
        responses.add(responses.POST, endpoint, body=make_response(FILES),
            content_type='application/json')

        files_dir = os.path.dirname(os.path.abspath(__file__))
        python = os.path.join(files_dir, 'files/python-powered.png')
        django = os.path.join(files_dir, 'files/django-project.gif')
        hello = os.path.join(files_dir, 'files/hello-world.txt')

        # Test multiple ways of passing in the file
        response = self.client.files.save(
            ('python-powered.png', open(python, 'rb')),
            ('django-project.gif', StringIO(open(django, 'rb').read())),
            ('hello-world.txt', open(hello, 'rb').read())
        )

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_file_delete(self):
        file = FILES[0]
        endpoint = 'https://testco.hexxie.com/api/v1/files/{0}/'.format(file['id'])
        responses.add(responses.DELETE, endpoint, status=204)

        self.client.files.remove(file['id'])
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint


class SchemaAPITests(MontageTests):
    @responses.activate
    def test_schema_list(self):
        endpoint = 'https://testco.hexxie.com/api/v1/schemas/'
        responses.add(responses.GET, endpoint, body=make_response(SCHEMAS),
            content_type='application/json')

        response = self.client.schemas.list()
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_schema_filter(self):
        endpoint = 'https://testco.hexxie.com/api/v1/schemas/'
        responses.add(responses.GET, endpoint, body=make_response(SCHEMAS),
            content_type='application/json')

        response = self.client.schemas.list(name__istartswith='m')
        assert len(responses.calls) == 1
        query = urlparse(responses.calls[0].request.url).query
        assert query == 'name__istartswith=m'

    @responses.activate
    def test_schema(self):
        schema = SCHEMAS[0]
        endpoint = 'https://testco.hexxie.com/api/v1/schemas/{0}/'.format(schema['name'])
        responses.add(responses.GET, endpoint, body=make_response(schema),
            content_type='application/json')

        response = self.client.schemas.get('movies')
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint


class UserAPITests(MontageTests):
    @responses.activate
    def test_user_list(self):
        endpoint = 'https://testco.hexxie.com/api/v1/users/'
        responses.add(responses.GET, endpoint, body=make_response([USER]),
            content_type='application/json')

        response = self.client.users.list()
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_user_filter(self):
        endpoint = 'https://testco.hexxie.com/api/v1/users/'
        responses.add(responses.GET, endpoint, body=make_response([USER]),
            content_type='application/json')

        response = self.client.users.list(email__endswith='example.com')
        assert len(responses.calls) == 1
        query = urlparse(responses.calls[0].request.url).query
        assert query == 'email__endswith=example.com'

    @responses.activate
    def test_create_user(self):
        endpoint = 'https://testco.hexxie.com/api/v1/users/'
        responses.add(responses.POST, endpoint, body=make_response(USER),
            content_type='application/json')

        response = self.client.users.create(
            full_name=USER['full_name'],
            email=USER['email'],
            password='letmein',
        )
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_update_user(self):
        endpoint = 'https://testco.hexxie.com/api/v1/users/1/'
        responses.add(responses.PATCH, endpoint, body=make_response(USER),
            content_type='application/json')

        response = self.client.users.update(USER['id'], password='changeme')
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint
        assert json.loads(responses.calls[0].request.body) == {'password': 'changeme'}

    @responses.activate
    def test_user_detail(self):
        endpoint = 'https://testco.hexxie.com/api/v1/users/1/'
        responses.add(responses.GET, endpoint, body=make_response(USER),
            content_type='application/json')

        response = self.client.users.get(1)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_user_detail(self):
        endpoint = 'https://testco.hexxie.com/api/v1/users/1/'
        responses.add(responses.DELETE, endpoint, status=204)

        response = self.client.users.remove(1)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint
