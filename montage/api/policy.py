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
