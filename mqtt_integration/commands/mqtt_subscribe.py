from django.core.management.base import BaseCommand
import paho.mqtt.client as mqtt

class Command(BaseCommand):
    help = 'Subscribe to an MQTT topic'

    def handle(self, *args, **options):
        client = mqtt.Client()

        def on_connect(client, userdata, flags, rc):
            print("Connected with result code " + str(rc))
            client.subscribe("your/topic")

        def on_message(client, userdata, msg):
            print(msg.topic + " " + str(msg.payload))

        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("mqtt.eclipse.org", 1883, 60)

        client.loop_forever()
