import responses
from ..utils import MontageTests, make_response, POLICY


class PolicyAPITests(MontageTests):
    @responses.activate
    def test_policy_list(self):
        endpoint = 'https://testco.hexxie.com/api/v1/policy/'
        responses.add(responses.GET, endpoint, body=make_response(POLICY),
            content_type='application/json')

        response = self.client.policies.list()
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_policy_detail(self):
        endpoint = 'https://testco.hexxie.com/api/v1/policy/{0}/'.format(POLICY['id'])
        responses.add(responses.GET, endpoint, body=make_response(POLICY),
            content_type='application/json')

        response = self.client.policies.get(POLICY['id'])
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_policy_update(self):
        endpoint = 'https://testco.hexxie.com/api/v1/policy/{0}/'.format(POLICY['id'])
        responses.add(responses.PATCH, endpoint, body=make_response(POLICY),
            content_type='application/json')

        response = self.client.policies.update(POLICY['id'], description='Updated')
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_policy_delete(self):
        endpoint = 'https://testco.hexxie.com/api/v1/policy/{0}/'.format(POLICY['id'])
        responses.add(responses.DELETE, endpoint, status=204)

        response = self.client.policies.remove(POLICY['id'])
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint
