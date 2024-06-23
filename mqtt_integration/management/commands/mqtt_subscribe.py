# mqtt_integration/management/commands/mqtt_subscribe.py
from django.core.management.base import BaseCommand
import asyncio
from mqtt_integration import subscribe

class Command(BaseCommand):
    help = 'Start the MQTT subscriber'

    def handle(self, *args, **kwargs):
        asyncio.run(subscribe.main())
