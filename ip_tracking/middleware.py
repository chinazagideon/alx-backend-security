"""
IP tracking middleware
"""

from django.http import HttpRequest
from .models import RequestLog

class IPTrackingMiddleware:
    """
    IP tracking middleware
    """
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request: HttpRequest):
        """
        Log the request
        """
        ip_address = request.META.get('REMOTE_ADDR')
        path = request.path
        RequestLog.objects.create(ip_address=ip_address, path=path)
        response = self.get_response(request)
        return response