from paho.mqtt import client as mqtt_client
import time
import ssl
Brocker = "a3aea2a70f7b43d1809561231ab50b37.s1.eu.hivemq.cloud"
port = 8883
client_id = "ESP8266Client-"
username = "ESP32"
password = "123456aA"
door_control_topic = "door_control"
led_control_topic = "led_control"
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        '''if rc == 0:
            print("Connected to the Broker")
        else:
            print(f"Failed to connect with code {rc}")'''

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2)

    return client

def publish(client, status):
    msg = status
    door_result = client.publish(door_control_topic, msg)
    led_result = client.publish(led_control_topic, msg)
    door_msg_status = door_result.rc
    led_msg_status = led_result.rc
    if door_msg_status == 0:
        print(f"Message: {msg} sent to topic {door_control_topic}")
    else:
        print(f"Failed to send message to topic {door_control_topic}")

    if led_msg_status == 0:
        print(f"Message: {msg} sent to topic {led_control_topic}")
    else:
        print(f"Failed to send message to topic {led_control_topic}")

def main():
    client = connect_mqtt()
    client.connect(Brocker, port)
    client.loop_start()  # Add this line to start the message loop in the background

    try:
        while True:
            door_status = input("Enter Door status (open/close): ")
            led_status = input("Enter Door status (on/off): ")
            publish(client, door_status)
            publish(client, led_status)
            time.sleep(2)  # Extend the sleep duration to allow the loop to handle messages
            
    except KeyboardInterrupt:
        print("Exiting...")
        client.loop_stop()  # Stop the background loop
        client.disconnect()

if __name__ == '__main__':
    main()
