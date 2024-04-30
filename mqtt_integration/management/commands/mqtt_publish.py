# mqtt_integration/management/commands/mqtt_publish.py
from django.core.management.base import BaseCommand
from mqtt_integration.publish import main as publish_main

from mqtt_integration import publish

class Command(BaseCommand):
    help = 'Publish MQTT messages'

    def handle(self, *args, **options):
        publish.main()
