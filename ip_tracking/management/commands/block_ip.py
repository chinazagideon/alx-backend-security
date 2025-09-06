"""
Block IP command
"""

from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    """
    Block IP command
    """

    def add_arguments(self, parser):
        """
        Add arguments to the command
        """
        parser.add_argument("ip_address", type=str)
        parser.add_argument("reason", type=str)
        
    def handle(self, *args, **options):
        """
        Handle the command
        """
        Block the IP
        """
        BlockedIP.objects.create(
            ip_address=options["ip_address"],
            reason=options["reason"]
        )
        self.stdout.write(self.style.SUCCESS(f"IP {options['ip_address']} blocked"))
    