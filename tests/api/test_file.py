import os
import responses
from ..utils import MontageTests, make_response, FILES

try:
    from cStringIO import StringIO
except ImportError:
    # Importing BytesIO as StringIO feels wrong...
    from io import BytesIO as StringIO

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def get_file_path(filename):
    path = os.path.join(os.path.dirname(__file__), '../files', filename)
    return os.path.abspath(path)


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

        python = get_file_path('python-powered.png')
        response = self.client.files.save(('python-powered.png', open(python, 'rb')))
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_file_upload_multiple(self):
        endpoint = 'https://testco.hexxie.com/api/v1/files/'
        responses.add(responses.POST, endpoint, body=make_response(FILES),
            content_type='application/json')

        python = get_file_path('python-powered.png')
        django = get_file_path('django-project.gif')
        hello = get_file_path('hello-world.txt')

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
