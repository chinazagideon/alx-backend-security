"""
IP tracking models
"""

from django.db import models

class RequestLog(models.Model):
    """
    Request log model
    """
    ip_address = models.GenericIPAddressField(unique=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.timestamp}"
    
class BlockedIP(models.Model):
    """
    Blocked IP model
    """
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.reason} - {self.timestamp}"

class SuspiciousIP(models.Model):
    """
    Suspicious IP model
    """
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    flagged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.reason} - {self.timestamp}"