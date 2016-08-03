import responses
from ..utils import MontageTests, make_response, SCHEMAS


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


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
    def test_schema_detail(self):
        schema = SCHEMAS[0]
        endpoint = 'https://testco.hexxie.com/api/v1/schemas/{0}/'.format(schema['name'])
        responses.add(responses.GET, endpoint, body=make_response(schema),
            content_type='application/json')

        response = self.client.schemas.get('movies')
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_schema_delete(self):
        schema = SCHEMAS[0]
        endpoint = 'https://testco.hexxie.com/api/v1/schemas/{0}/'.format(schema['name'])
        responses.add(responses.DELETE, endpoint, status=204)

        response = self.client.schemas.remove(schema['name'])
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint
