import json

import logging
import time

logger = logging.getLogger(__name__)


class APILogMiddleware:
    """
    Middleware for logging api requests
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        if request.path.startswith('/api/'):
            response_ms = (time.time() - start) * 1000
            method = request.method
            status_code = response.status_code
            request_path = request.path
            data = json.dumps(response.data)
            logger.info({
                'method': method,
                'path': request_path,
                'time': f'{response_ms:.3f} ms',
                'status_code': status_code,
                'response_data': data
            })
        return response
