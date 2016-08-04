import warnings


class SchemaAPI(object):
    def __init__(self, client):
        self.client = client

    def create(self, name, fields=None):
        payload = {
            'name': name,
            'fields': fields or []
        }
        return self.client.request('schemas', method='post', json=payload)

    def list(self, **kwargs):
        return self.client.request('schemas', params=kwargs)

    def get(self, schema):
        return self.client.request('schemas/{0}'.format(schema))

    def update(self, schema, name=None, fields=None):
        payload = {}
        if name:
            payload['name'] = name
        if fields:
            payload['fields'] = fields

        if payload:
            return self.client.request('schemas/{0}'.format(schema),
                method='patch', json=payload)

    def delete(self, schema):
        return self.client.request('schemas/{0}'.format(schema), method='delete')

    def remove(self, schema):
        warnings.warn('The function remove() is deprecated, use delete().',
        DeprecationWarning, stacklevel=2)
        return self.delete(schema)
