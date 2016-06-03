

class Command(object):
    def __init__(self, script, env=None, output='text', args=None, timeout=5000):
        self.script = script
        self.env = env or {}
        self.output = output
        self.args = args or []
        self.timeout = timeout

    def as_dict(self):
        return {
            '$type': 'command',
            '$script': self.script,
            '$env': self.env,
            '$output': self.output,
            '$args': self.args,
            '$timeout': self.timeout,
        }
