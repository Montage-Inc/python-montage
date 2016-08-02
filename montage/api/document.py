class DocumentAPI(object):
    def __init__(self, client):
        self.client = client

    def save(self, schema, *documents):
        endpoint = 'schemas/{0}/documents'.format(schema, schema)
        return self.client.request(endpoint, method='post', json=documents)

    def get(self, schema, document_id):
        endpoint = 'schemas/{0}/documents/{1}'.format(schema, document_id)
        return self.client.request(endpoint)

    def replace(self, schema, document):
        endpoint = 'schemas/{0}/documents/{1}'.format(schema, document['id'])
        return self.client.request(endpoint, method='put', json=document)

    def update(self, schema, document):
        endpoint = 'schemas/{0}/documents/{1}'.format(schema, document['id'])
        return self.client.request(endpoint, method='patch', json=document)

    def remove(self, schema, document_id):
        endpoint = 'schemas/{0}/documents/{1}'.format(schema, document_id)
        return self.client.request(endpoint, method='delete')
