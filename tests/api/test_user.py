import json
import responses
from ..utils import MontageTests, make_response, USER


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


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
    def test_user_delete(self):
        endpoint = 'https://testco.hexxie.com/api/v1/users/1/'
        responses.add(responses.DELETE, endpoint, status=204)

        response = self.client.users.delete(1)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint
