

class SchedulerAPI(object):
    def __init__(self, client):
        self.client = client

    def create(self, crontab, command):
        payload = {
            'crontab': crontab,
            'command': command
        }
        return self.client.request('scheduled-tasks', method='post', json=payload)

    def list(self, **kwargs):
        return self.client.request('scheduled-tasks', params=kwargs)

    def get(self, task_id):
        return self.client.request('scheduled-tasks/{0}'.format(task_id))

    def update(self, task_id, crontab=None, command=None):
        payload = {}
        if crontab:
            payload['crontab'] = crontab
        if command:
            payload['command'] = command

        if payload:
            return self.client.request('scheduled-tasks/{0}'.format(task_id),
                method='patch', json=payload)

    def delete(self, task_id):
        return self.client.request('scheduled-tasks/{0}'.format(task_id), method='delete')
