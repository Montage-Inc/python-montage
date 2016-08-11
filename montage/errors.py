
__all__ = ('MontageError', 'HttpError')


class MontageError(Exception):
    pass


class HttpError(MontageError):
    def __init__(self, response, message):
        self.response = response
        self.message = message

    @property
    def status_code(self):
        return self.response.status_code
