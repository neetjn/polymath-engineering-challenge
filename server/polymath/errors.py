class PolymathException(Exception):
    status_code = 500
    message = 'An internal error has occurred'

    def __init__(self, msg=None):
        super().__init__(self)
        self.message = msg or self.message

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class ExternalResourcesNotFound(PolymathException):
    status_code = 404
    message = 'External resources was not found'

class ExternalResourcesNotFound(PolymathException):
    status_code = 404
    message = 'External resource was not found'
