import responses
from ..utils import MontageTests, make_response, DOCUMENTS


class DocumentAPITests(MontageTests):
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
