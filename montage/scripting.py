

class Script(object):
    def __init__(self, name):
        self.name = name

    def as_dict(self):
        return {
            '$type': 'script',
            '$name': self.name
        }


class RunLua(object):
    def __init__(self, code):
        self.code = code

    def as_dict(self):
        return {
            '$type': 'lua',
            '$code': self.code
        }
