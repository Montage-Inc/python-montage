import responses

from .utils import MontageTests


class SchemaAPITests(MontageTests):
    @responses.activate
    def test_all_schemas(self):
        import ipdb
        ipdb.set_trace()
