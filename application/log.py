import json

from django.http import HttpRequest
from rest_framework.response import Response


def create_log_message(request: HttpRequest, response: Response, start_time: float, end_time: float) -> dict:
    """
    Create message in dict format
    """
    response_ms = (end_time - start_time) * 1000
    method = request.method
    status_code = response.status_code
    request_path = request.path
    response_data = json.dumps(response.data)
    return {
        'method': method,
        'path': request_path,
        'time': f'{response_ms:.3f} ms',
        'status_code': status_code,
        'response_data': response_data
    }
