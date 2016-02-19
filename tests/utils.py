import montage
import unittest


class MontageTests(unittest.TestCase):
    def setUp(self):
        self.client = montage.Client('testco', url='hexxie.com')
        super(MontageTests, self).setUp()
