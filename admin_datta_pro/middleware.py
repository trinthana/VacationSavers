from .threadlocals import thread_locals

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_locals.request = request
        try:
            if thread_locals.token is None :
                thread_locals.token = request.session['token']
        except:
            thread_locals.token = None

        response = self.get_response(request)
        return response
