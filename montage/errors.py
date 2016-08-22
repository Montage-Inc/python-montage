
__all__ = ('MontageError', 'HttpError')


class MontageError(Exception):
    def __init__(self, message):
        self.message = message


class HttpError(MontageError):
    def __init__(self, message, response):
        self.response = response
        super(HttpError, self).__init__(message)

    @property
    def status_code(self):
        return self.response.status_code
