"""
IP tracking middleware
"""

from django.http import HttpRequest, HttpResponse
from django.core.cache import cache
from .models import RequestLog, BlockedIP


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

        # Check if the IP is blocked
        if BlockedIP.objects.filter(
            ip_address=request.META.get("REMOTE_ADDR")
        ).exists():
            return HttpResponse(status=403, content="IP is blocked")
        
        #return geolocation data from cache if ip address is in cache
        geolocation = cache.get(request.META.get("REMOTE_ADDR"))
        if not geolocation:
            #get geolocation data from the request
            geolocation = request.geolocation
            #set geolocation data in cache for 24 hours
            cache.set(request.META.get("REMOTE_ADDR"), geolocation, timeout=60 * 60 * 24)

        # Log the request
        ip_address = request.META.get("REMOTE_ADDR")
        path = request.path

        # Get the geolocation data from the cache if not in cache, get it from the request
        country = geolocation.get("country")
        city = geolocation.get("city")

        # Log the request
        RequestLog.objects.create(
            ip_address=ip_address, 
            path=path, 
            country=country, 
            city=city
        )

        # Get the response
        response = self.get_response(request)
        return response
