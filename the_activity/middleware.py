from .signals import create_log_entry


class ActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.create_log_entry = create_log_entry
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
