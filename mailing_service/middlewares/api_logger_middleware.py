import pathlib
import time
import logging

import mailing_service.logging.log_messages_creator as log

from django.http import HttpRequest
from rest_framework.response import Response

logging.basicConfig(filename=pathlib.Path(__file__).resolve().parent.parent.joinpath('logging/logger.log'),
                    format='%(levelname)s %(asctime)s %(message)s', level=logging.INFO)


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
        try:
            if request.path.startswith('/api/'):
                logging.info(log.create_api_log_message(request, response, start, end))
        except Exception:
            pass
        return response
