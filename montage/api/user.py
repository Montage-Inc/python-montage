import warnings


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

    def delete(self, user_id):
        return self.client.request('users/{0}'.format(user_id), method='delete')

    def remove(self, user_id):
        warnings.warn('The function remove() is deprecated, use delete().',
        DeprecationWarning, stacklevel=2)
        return self.delete(user_id)
