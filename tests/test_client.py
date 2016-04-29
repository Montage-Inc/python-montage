import json
import montage
import responses

from .utils import MontageTests, make_response, USER


class ClientTests(MontageTests):
    def test_url(self):
        url1 = 'https://testco.hexxie.com/api/v1/user/'
        url2 = self.client.url('user')
        self.assertEqual(url1, url2)

    def get_test_client(self):
        client = montage.Client('testco')
        client.host = 'hexxie.com'
        return client

    @responses.activate
    def test_authenticate(self):
        endpoint = 'https://testco.hexxie.com/api/v1/user/'
        responses.add(responses.POST, endpoint, body=make_response(USER),
            content_type='application/json')

        client = self.get_test_client()
        assert client.token is None

        authenticated = client.authenticate('test@example.com', 'letmein')
        assert authenticated is True
        assert client.token == USER['token']
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_authenticate_invalid(self):
        error = {'errors': [{'detail': 'Incorrect authentication credentials.'}]}
        endpoint = 'https://testco.hexxie.com/api/v1/user/'
        responses.add(responses.POST, endpoint, body=json.dumps(error),
            content_type='application/json')

        client = self.get_test_client()
        assert client.token is None

        authenticated = client.authenticate('fake@example.com', 'invalid')
        assert authenticated is False
        assert client.token is None
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    def test_user_unauthenticated(self):
        client = self.get_test_client()
        assert client.user() is None

    @responses.activate
    def test_user_authenticated(self):
        endpoint = 'https://testco.hexxie.com/api/v1/user/'
        responses.add(responses.GET, endpoint, body=make_response(USER),
            content_type='application/json')

        response = self.client.user()
        assert response['data'] == USER

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint
