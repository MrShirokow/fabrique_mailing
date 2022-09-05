import hashlib
import hmac

from django.http import HttpResponseForbidden, HttpRequest, HttpResponse

from config.settings import API_SECRET


class ApiSecretMiddleware:
    """
    Middleware checks that the API_SECRET from the request matches the secret from settings.py
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path.startswith('/api/'):
            if request.headers.get('X-Signature') != get_signature(request, API_SECRET):
                return HttpResponseForbidden('Unknown API key')

        return self.get_response(request)


def get_signature(request: HttpRequest, key: str):
    """
    Get api key signature for protection
    """
    request_str = f'{request.method}\n{request.path}\n{request.headers}'
    return hmac.new(key.encode(), request_str.encode(), hashlib.sha256).hexdigest()
