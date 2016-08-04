

class TaskAPI(object):
    def __init__(self, client):
        self.client = client

    def run(self, command, image=None, token=None, time_limit=None):
        payload = {'command': command}
        if image:
            payload['image'] = image
        if token:
            payload['token'] = token
        if time_limit:
            payload['time_limit'] = time_limit
        return self.client.request('tasks',
            method='post', json=payload)

    def get(self, task_id):
        return self.client.request('tasks/{0}'.format(task_id))
