import time
import logging

import application.log as log

from django.http import HttpRequest
from rest_framework.response import Response


logger = logging.getLogger(__name__)


class APILogMiddleware:
    """
    Middleware for logging api requests
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> Response:
        start = time.time()
        response = self.get_response(request)
        end = time.time()
        if request.path.startswith('/api/'):
            logger.info(log.create_api_log_message(request, response, start, end))
        return response
