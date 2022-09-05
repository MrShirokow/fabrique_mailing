import json

from django.http import HttpRequest
from requests.models import Response, PreparedRequest
from rest_framework.response import Response as RestResponse


def create_api_log_message(request: HttpRequest, response: RestResponse, start_time: float, end_time: float) -> dict:
    """
    Create message in dict format
    """
    response_ms = (end_time - start_time) * 1000
    return {
        'method': request.method,
        'path': request.path,
        'time': f'{response_ms:.3f} ms',
        'status_code': response.status_code,
        'response_data': json.dumps(response.data),
    }


def create_mailing_log_message(request: PreparedRequest, response: Response) -> dict:
    return {
        'method': request.method,
        'path': request.path_url,
        'status_code': response.status_code,
        'response_data': response.text,
    }
