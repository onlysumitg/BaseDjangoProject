
from threading import local


class TheSystemMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.search_value = request.GET.get('search_value', "").strip()
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


_user = local()

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        _user.value = request.user
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

def get_current_user():
    return _user.value