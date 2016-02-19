import montage

from .utils import MontageTests


class QueryTests(MontageTests):
    def test_url(self):
        url1 = 'https://testco.hexxie.com/api/v1/auth/user/'
        url2 = self.client.url('auth/user')
        self.assertEqual(url1, url2)

    def test_authenticate(self):
        pass

    def test_user(self):
        pass
