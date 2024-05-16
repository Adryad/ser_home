from django.apps import AppConfig
from django.core.management import call_command
import threading

class MqttIntegrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqtt_integration'
    def ready(self):
        # Run the MQTT subscribe command in a separate thread to avoid blocking the main thread
        thread = threading.Thread(target=self.start_mqtt_subscribe)
        thread.start()

    def start_mqtt_subscribe(self):
        call_command('mqtt_subscribe')
