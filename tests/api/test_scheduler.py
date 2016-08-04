import responses
from ..utils import MontageTests, make_response, SCHEDULED_TASKS


class SchedulerAPITests(MontageTests):
    @responses.activate
    def test_task_list(self):
        endpoint = 'https://testco.hexxie.com/api/v1/scheduled-tasks/'
        responses.add(responses.GET, endpoint, body=make_response(SCHEDULED_TASKS),
            content_type='application/json')

        response = self.client.scheduler.list()
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_create_task(self):
        SCHEDULED_TASK = SCHEDULED_TASKS[0]
        endpoint = 'https://testco.hexxie.com/api/v1/scheduled-tasks/'
        responses.add(responses.POST, endpoint, body=make_response(SCHEDULED_TASK),
            content_type='application/json')

        response = self.client.scheduler.create(
            crontab=SCHEDULED_TASK['crontab'],
            command=SCHEDULED_TASK['command'],
        )
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_task_detail(self):
        SCHEDULED_TASK = SCHEDULED_TASKS[0]
        endpoint = 'https://testco.hexxie.com/api/v1/scheduled-tasks/{0}/'.format(SCHEDULED_TASK['id'])
        responses.add(responses.GET, endpoint, body=make_response(SCHEDULED_TASKS),
            content_type='application/json')

        response = self.client.scheduler.get(SCHEDULED_TASK['id'])
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_task_update(self):
        SCHEDULED_TASK = SCHEDULED_TASKS[0]
        endpoint = 'https://testco.hexxie.com/api/v1/scheduled-tasks/{0}/'.format(SCHEDULED_TASK['id'])
        responses.add(responses.PATCH, endpoint, body=make_response(SCHEDULED_TASK),
            content_type='application/json')

        response = self.client.scheduler.update(SCHEDULED_TASK['id'], crontab='0 * * * *')
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_task_delete(self):
        SCHEDULED_TASK = SCHEDULED_TASKS[0]
        endpoint = 'https://testco.hexxie.com/api/v1/scheduled-tasks/{0}/'.format(SCHEDULED_TASK['id'])
        responses.add(responses.DELETE, endpoint, status=204)

        response = self.client.scheduler.delete(SCHEDULED_TASK['id'])
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint
