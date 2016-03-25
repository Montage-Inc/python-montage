import mimetypes

__all__ = ('DataAPI', 'FileAPI', 'RoleAPI', 'SchemaAPI')


class DocumentsAPI(object):
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


class FileAPI(object):
    def __init__(self, client):
        self.client = client

    def list(self, **kwargs):
        return self.client.request('files', params=kwargs)

    def get(self, file_id):
        endpoint = 'files/{0}'.format(file_id)
        return self.client.request(endpoint)

    def remove(self, file_id):
        endpoint = 'files/{0}'.format(file_id)
        return self.client.request(endpoint, method='delete')

    def save(self, *files):
        '''
            Each file is extected to be a tuple of (name, content), where
            content is a file-like object or the contents as a string.

            client.files.save(('foo.txt', open('/path/to/foo.txt')))
            client.files.save(('foo.txt', StringIO('This is foo.txt')))
            client.files.save(('foo.txt', 'This is foo.txt'))
        '''
        file_list = []
        for name, contents in files:
            content_type = mimetypes.guess_type(name)[0]
            file_list.append(('file', (name, contents, content_type)))
        return self.client.request('files', 'post', files=file_list)


class PolicyAPI(object):
    def __init__(self, client):
        self.client = client

    def create(self, description, policy):
        payload = {
            'description': description,
            'policy': policy
        }
        return self.client.request('policy', method='post', json=payload)

    def list(self, **kwargs):
        return self.client.request('policy', params=kwargs)

    def get(self, policy_id):
        return self.client.request('policy/{0}'.format(policy_id))

    def update(self, policy_id, description=None, policy=None):
        payload = {}
        if description:
            payload['description'] = description
        if policy:
            payload['policy'] = policy

        if payload:
            return self.client.request('policy/{0}'.format(policy_id),
                method='patch', json=payload)

    def remove(self, policy_id):
        return self.client.request('policy/{0}'.format(policy_id), method='delete')

    def check_permission(self, action, resource=None):
        payload = {
            'action': action,
            'resource': resource,
        }
        return self.client.request('policy/check/', params=payload)


class RoleAPI(object):
    def __init__(self, client):
        self.client = client

    def create(self, name, add_users=None):
        payload = {
            'name': name,
            'add_users': users or []
        }
        return self.client.request('roles', method='post', json=payload)

    def list(self, **kwargs):
        return self.client.request('roles', params=kwargs)

    def get(self, role):
        return self.client.request('roles/{0}'.format(role))

    def update(self, role, name=None, add_users=None, remove_users=None):
        payload = {}
        if name:
            payload['name'] = name
        if add_users:
            payload['add_users'] = add_users
        if remove_users:
            payload['remove_users'] = remove_users

        if payload:
            return self.client.request('roles/{0}'.format(role),
                method='patch', json=payload)

    def remove(self, role):
        return self.client.request('roles/{0}'.format(role), method='delete')


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

    def remove(self, schema):
        return self.client.request('schemas/{0}'.format(schema), method='delete')


class UserAPI(object):
    attributes = ('email', 'full_name', 'password')

    def __init__(self, client):
        self.client = client

    def list(self, **kwargs):
        return self.client.request('users', params=kwargs)

    def create(self, full_name, email, password):
        payload = {
            'full_name': full_name,
            'email': email,
            'password': password,
        }
        return self.client.request('users', method='post', json=payload)

    def get(self, user_id):
        return self.client.request('users/{0}'.format(user_id))

    def update(self, user_id, full_name=None, email=None, password=None):
        payload = {}
        if full_name:
            payload['full_name'] = full_name
        if email:
            payload['email'] = email
        if password:
            payload['password'] = password

        if payload:
            return self.client.request('users/{0}'.format(user_id),
                method='patch', json=payload)

    def remove(self, user_id):
        return self.client.request('users/{0}'.format(user_id), method='delete')
