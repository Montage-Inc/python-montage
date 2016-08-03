import montage
import pytest

from .utils import MontageTests

class CommandTests(MontageTests):
    def test_command(self):
        command = montage.Command('fetch_ratings.lua', output='json')
        expected = {
            '$type': 'command',
            '$script': 'fetch_ratings.lua',
            '$env': {},
            '$args': [],
            '$output': 'json',
            '$timeout': 5000,
        }

        assert command.script == 'fetch_ratings.lua'
        assert command.as_dict() == expected
