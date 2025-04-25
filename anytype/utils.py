from functools import wraps


def requires_auth(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self._apiEndpoints is None:
            raise Exception("You need to auth first")
        return method(self, *args, **kwargs)

    return wrapper
