import json
import requests

from .error import StytchError


def throw_stytch_exception(func):
    def wrapper(*args, **kwargs):
        resp: requests.models.Response = func(*args, **kwargs)
        if resp.status_code >= 400:
             raise StytchError(**json.loads(resp._content))
        else:
            return resp

    return wrapper
