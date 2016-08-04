import responses
from ..utils import MontageTests, make_response, ROLE


class RoleAPITests(MontageTests):
    @responses.activate
    def test_role_list(self):
        endpoint = 'https://testco.hexxie.com/api/v1/roles/'
        responses.add(responses.GET, endpoint, body=make_response(ROLE),
            content_type='application/json')

        response = self.client.roles.list()
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_role_detail(self):
        endpoint = 'https://testco.hexxie.com/api/v1/roles/{0}/'.format(ROLE['name'])
        responses.add(responses.GET, endpoint, body=make_response(ROLE),
            content_type='application/json')

        response = self.client.roles.get(ROLE['name'])
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_role_update(self):
        endpoint = 'https://testco.hexxie.com/api/v1/roles/{0}/'.format(ROLE['name'])
        responses.add(responses.PATCH, endpoint, body=make_response(ROLE),
            content_type='application/json')

        response = self.client.roles.update(ROLE['name'], name='Managers')
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_role_delete(self):
        endpoint = 'https://testco.hexxie.com/api/v1/roles/{0}/'.format(ROLE['name'])
        responses.add(responses.DELETE, endpoint, status=204)

        response = self.client.roles.delete(ROLE['name'])
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint
