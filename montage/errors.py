
__all__ = ('MontageError', 'HttpError')


class MontageError(Exception):
    pass


class HttpError(MontageError):
    def __init__(self, status_code, response):
        self.status_code = status_code
        self.response = response
