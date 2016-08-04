import responses

from ..utils import MontageTests, make_response


class TaskAPITests(MontageTests):
    @responses.activate
    def test_make_task(self):
        endpoint = 'https://testco.hexxie.com/api/v1/tasks/'
        responses.add(responses.POST, endpoint, body=make_response({}),
            content_type='application/json')

        response = self.client.tasks.run("hello.py")
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint

    @responses.activate
    def test_get_task(self):
        endpoint = 'https://testco.hexxie.com/api/v1/tasks/some-task-id/'
        responses.add(responses.GET, endpoint, body=make_response({}),
            content_type='application/json')

        response = self.client.tasks.get("some-task-id")
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == endpoint
