

class ProjectAPI(object):
    def __init__(self, client):
        self.client = client

    def get(self):
        return self.client.request('project')

    def update(self, name=None, subdomain=None):
        payload = {}
        if name:
            payload['name'] = name
        if subdomain:
            payload['subdomain'] = subdomain

        if payload:
            return self.client.request('project',
                method='patch', json=payload)
