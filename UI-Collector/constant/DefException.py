class RestartException(Exception):
    def __init__(self, message):
        super().__init__(message)


class TerminateException(Exception):
    def __init__(self, message):
        super().__init__(message)


class TimeLimitException(Exception):
    def __init__(self, message):
        super().__init__(message)