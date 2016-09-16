import warnings


class RoleAPI(object):
    def __init__(self, client):
        self.client = client

    def create(self, name, add_users=None):
        payload = {
            'name': name,
            'add_users': add_users or []
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

    def delete(self, role):
        return self.client.request('roles/{0}'.format(role), method='delete')

    def remove(self, role):
        warnings.warn('The function remove() is deprecated, use delete().',
        DeprecationWarning, stacklevel=2)
        return self.delete(role)
