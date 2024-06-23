# mqtt_integration/subscribe.py
from paho.mqtt import client as mqtt_client
import ssl
import requests
import os
import django
import time
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')
django.setup()

Broker = "a3aea2a70f7b43d1809561231ab50b37.s1.eu.hivemq.cloud"
port = 8883
client_id = "ESP8266Client_Postman"
username = "ESP32"
password = "123456aA"
humidity_topic = "humidity"
temperature_celsius_topic = "temperature_celsius"
Gas_topic = "Gas_level"
Rain_Status = "Rain_ST"

# API endpoint to post data
api_url = "https://ser-home-2.onrender.com/numericaldata/"

data_payload = {
    'user_id': 'test_user',  # Replace with actual user ID
    'temperature': None,
    'humidity': None,
    'gas_level': None,
    'rain': None,
    'timestamp': datetime.now().isoformat(),
}

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

    client = mqtt_client.Client(client_id=client_id, protocol=mqtt_client.MQTTv311)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message_callback

    # Disable certificate verification for testing (not recommended for production)
    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2)
    client.tls_insecure_set(True)

    return client

def on_message(client, userdata, msg):
    global data_payload
    print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
    
    if msg.topic == temperature_celsius_topic:
        data_payload['temperature'] = float(msg.payload.decode())
    elif msg.topic == humidity_topic:
        data_payload['humidity'] = float(msg.payload.decode())
    elif msg.topic == Gas_topic:
        data_payload['gas_level'] = float(msg.payload.decode())
    elif msg.topic == Rain_Status:
        data_payload['rain'] = bool(int(msg.payload.decode()))
    
    # Post data to the NumericalDataListCreate API if all fields are filled
    if all(value is not None for value in data_payload.values()):
        response = requests.post(api_url, json=data_payload)
        if response.status_code == 201:
            print("Data posted successfully")
        else:
            print(f"Failed to post data: {response.status_code} - {response.text}")

def main():
    client = connect_mqtt(on_message)
    client.connect(Broker, port)
    client.loop_start()
    time.sleep(15)  # Adjust the sleep time as necessary to gather enough data
    client.loop_stop()

if __name__ == '__main__':
    main()
