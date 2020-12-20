import logging
import traceback

class InternalServerErrorMiddleware:
    """
    Logs internal server errors and sends email to admin.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("")

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code >= 500:
            self.logger.error(str(traceback.extract_stack()))
        return response
