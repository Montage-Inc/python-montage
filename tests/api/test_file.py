import os
import responses
from ..utils import MontageTests, make_response, FILES


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
