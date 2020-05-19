class TaurosAPIException(Exception):
    """
    Base class for all exceptions
    """
    pass


class ValidationError(TaurosAPIException):
    pass
