import responses
from ..utils import MontageTests, make_response, PROJECT


class ProjectAPITests(MontageTests):
    @responses.activate
    def test_role_detail(self):
        endpoint = 'https://testco.hexxie.com/api/v1/project/'
        responses.add(responses.GET, endpoint, body=make_response(PROJECT),
            content_type='application/json')

        response = self.client.project.get()
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_role_update(self):
        endpoint = 'https://testco.hexxie.com/api/v1/project/'
        responses.add(responses.PATCH, endpoint, body=make_response(PROJECT),
            content_type='application/json')

        response = self.client.project.update(name='Test-Co', subdomain='test-co')
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint
