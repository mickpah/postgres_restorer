from .utils import dict_to_str


class PG_Error(Exception):
    def __init__(self, message=None, payload=None, code=None):
        self.message = message
        self.payload = payload
        self.code = code

    def __str__(self):
        _str = []

        if self.message:
            _str.append(f'message: {self.message}')

        if self.payload:
            _str.append(f'payload: {self.payload}')

        if self.code:
            _str.append(f'code: {self.code}')

        return '\n'.join(_str)


class PG_ConnectionError(PG_Error):
    def __init__(self, traceback_details):
        self.traceback_details = traceback_details

    def __str__(self):
        return dict_to_str(self.traceback_details)
