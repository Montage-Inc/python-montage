import montage
import responses

from .utils import MontageTests, make_response, USER


class QueryTests(MontageTests):
    def test_url(self):
        url1 = 'https://testco.hexxie.com/api/v1/auth/user/'
        url2 = self.client.url('auth/user')
        self.assertEqual(url1, url2)

    @responses.activate
    def test_authenticate(self):
        endpoint = 'https://testco.hexxie.com/api/v1/auth/'
        responses.add(responses.POST, endpoint, body=make_response(USER),
            content_type='application/json')

        self.client.authenticate('test@example.com', 'letmein')

        assert self.client.token == USER['token']

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    def test_user(self):
        pass
