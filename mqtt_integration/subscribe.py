from paho.mqtt import client as mqtt_client
import ssl
Brocker = "a3aea2a70f7b43d1809561231ab50b37.s1.eu.hivemq.cloud"
port = 8883
client_id = "ESP8266Client_1"
username = "ESP32"
password = "123456aA"
humidity_topic = "humidity"
temperature_celsius_topic = "temperature_celsius"
Gas_topic = "Gas_level"

def connect_mqtt(on_message_callback):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to the Broker")
            client.subscribe(temperature_celsius_topic)
            client.subscribe(humidity_topic)
            client.subscribe(Gas_topic)
        else:
            print(f"Failed to connect with code {rc}")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message_callback
    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2)

    return client

def on_message(client, userdata, msg):
    print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")

def main():
    client = connect_mqtt(on_message)
    client.connect(Brocker, port)
    client.loop_forever()

if __name__ == '__main__':
    main()