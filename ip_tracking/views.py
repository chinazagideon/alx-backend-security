"""
Views for the ip_tracking app
"""

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit

def get_rate(group, request):
    """
    Get the rate for a given group
    """
    if request.user.is_authenticated:
        return '10/m' 
    else:
        return '5/m'
    
@ratelimit(key='ip', rate=get_rate, block=True)
def login_view(request):
    """
    Login view
    """
    return HttpResponse("Login view")

@ratelimit(key='ip', rate=get_rate, block=True)
def register_view(request):
    """
    Register view
    """
    return HttpResponse("Register view")