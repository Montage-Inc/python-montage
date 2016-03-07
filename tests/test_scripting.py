import montage
import pytest

from .utils import MontageTests

class ScriptingTests(MontageTests):
    def test_script(self):
        script = montage.Script('fetch_ratings.lua')
        expected = {
            '$type': 'script',
            '$name': 'fetch_ratings.lua'
        }

        assert script.name == 'fetch_ratings.lua'
        assert script.as_dict() == expected

    def test_lua(self):
        source_code = '''
            function()
                return "hello, world"
            end
        '''
        script = montage.RunLua(source_code)
        expected = {
            '$type': 'lua',
            '$code': source_code
        }

        assert script.code == source_code
        assert script.as_dict() == expected
