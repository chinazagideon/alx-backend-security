"""
Handle Async tasks
"""
from celery import shared_task
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def flag_suspicious_ips(ip_address, reason):
    """
    Flag a suspicious IP
    """

    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Find IPs with high request counts
    high_traffic_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago
    ).values('ip_address').annotate(
        request_count=Count('ip_address')
    ).filter(
        request_count__gte=100
    )

    for entry in high_traffic_ips:
        ip = entry['ip_address']
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            defaults = {'reason': 'Exceeded 100 requests per hour'}
        )
    

    #Find IPs that accessed sensitive paths
    sensitive_paths = ['/admin', '/login']
    sensitive_access_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values('ip_address').distinct()

    for entry in sensitive_access_ips:
        ip = entry['ip_address']
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            defaults = {'reason': 'Accessed sensitive paths'}
        )