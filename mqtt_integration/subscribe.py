# mqtt_integration/subscribe.py
import os
import django
import ssl
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')
django.setup()

from paho.mqtt import client as mqtt_client
from django.core.cache import cache
from mqtt_integration.models import NumericalData

Broker = "a3aea2a70f7b43d1809561231ab50b37.s1.eu.hivemq.cloud"
port = 8883
client_id = "ESP8266Client_Postman"
username = "ESP32"
password = "123456aA"
humidity_topic = "humidity"
temperature_celsius_topic = "temperature_celsius"
Gas_topic = "Gas_level"
Rain_Status = "Rain_ST"

def connect_mqtt(on_message_callback):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to the Broker")
            client.subscribe(temperature_celsius_topic)
            client.subscribe(humidity_topic)
            client.subscribe(Gas_topic)
            client.subscribe(Rain_Status)
        else:
            print(f"Failed to connect with code {rc}")

    client = mqtt_client.Client(client_id=client_id, callback_api_version=5)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message_callback
    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2)

    return client

def on_message(client, userdata, msg):
    print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
    if msg.topic == humidity_topic:
        cache.set('humidity', msg.payload.decode(), timeout=None)
    elif msg.topic == temperature_celsius_topic:
        cache.set('temperature_celsius', msg.payload.decode(), timeout=None)
    elif msg.topic == Gas_topic:
        cache.set('Gas_level', msg.payload.decode(), timeout=None)
    elif msg.topic == Rain_Status:
        cache.set('Rain_ST', msg.payload.decode(), timeout=None)

    # Post data to API
    payload = {
        'user_id': 'some_user_id',
        'temperature': cache.get('temperature_celsius'),
        'humidity': cache.get('humidity'),
        'gas_level': cache.get('Gas_level'),
        'rain': cache.get('Rain_ST')
    }
    try:
        response = requests.post('https://your-deployment-url.com/numericaldata/', json=payload)
        if response.status_code != 201:
            print(f"Failed to post data: {response.status_code} - {response.content.decode()}")
    except Exception as e:
        print(f"Error posting data: {str(e)}")

def main():
    client = connect_mqtt(on_message)
    client.connect(Broker, port)
    client.loop_forever()

if __name__ == '__main__':
    main()
