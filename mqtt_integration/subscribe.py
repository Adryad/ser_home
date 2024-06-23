# mqtt_integration/subscribe.py
from paho.mqtt import client as mqtt_client
import ssl
import requests
import os
import django
import logging
from datetime import datetime
import asyncio

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')
django.setup()

# MQTT Broker configuration
Broker = "a3aea2a70f7b43d1809561231ab50b37.s1.eu.hivemq.cloud"
port = 8883
client_id = "ESP8266Client_Postman"
username = "ESP32"
password = "123456aA"
topics = ["humidity", "temperature_celsius", "Gas_level", "Rain_ST"]

# API endpoint to post data
api_url = "https://ser-home-2.onrender.com/numericaldata/"

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data payload template
data_payload = {
    'user_id': 'test_user',  # Replace with actual user ID
    'temperature': None,
    'humidity': None,
    'gas_level': None,
    'rain': None,
    'timestamp': datetime.now().isoformat(),
}

# Last received values
last_values = {
    'temperature': None,
    'humidity': None,
    'gas_level': None,
    'rain': None
}

def connect_mqtt(on_message_callback):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to the Broker")
            for topic in topics:
                client.subscribe(topic)
        else:
            logger.error(f"Failed to connect with code {rc}")

    client = mqtt_client.Client(client_id=client_id, protocol=mqtt_client.MQTTv311)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message_callback

    # Disable certificate verification for testing (not recommended for production)
    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2)
    client.tls_insecure_set(True)

    return client

def on_message(client, userdata, msg):
    global data_payload, last_values
    logger.info(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
    
    try:
        value = msg.payload.decode()
        if msg.topic == "temperature_celsius":
            data_payload['temperature'] = float(value)
        elif msg.topic == "humidity":
            data_payload['humidity'] = float(value)
        elif msg.topic == "Gas_level":
            data_payload['gas_level'] = float(value)
        elif msg.topic == "Rain_ST":
            data_payload['rain'] = bool(int(value))

        if last_values[msg.topic.split('_')[0]] != value:
            last_values[msg.topic.split('_')[0]] = value
            if all(v is not None for v in data_payload.values()):
                response = requests.post(api_url, json=data_payload)
                if response.status_code == 201:
                    logger.info("Data posted successfully")
                else:
                    logger.error(f"Failed to post data: {response.status_code} - {response.text}")
        else:
            logger.info(f"Duplicate data '{value}' for topic '{msg.topic}' not posted")

    except ValueError as e:
        logger.error(f"Error processing message: {e}")

async def main():
    client = connect_mqtt(on_message)
    client.connect(Broker, port)
    client.loop_start()

    try:
        while True:
            await asyncio.sleep(15)  # Adjust the sleep time as necessary
    except KeyboardInterrupt:
        logger.info("Stopping MQTT client...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
