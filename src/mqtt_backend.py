from paho.mqtt import client as mqtt_client

import settings
from sales_man_helper import process_sales_man


def connect_inbound_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(settings.INBOUND_CLIENT_ID)
    client.on_connect = on_connect
    client.connect(settings.MQTT_BROKER, settings.MQTT_PORT)
    return client


def connect_outbound_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(settings.OUTBOUND_CLIENT_ID)
    client.on_connect = on_connect
    client.connect(settings.MQTT_BROKER, settings.MQTT_PORT)
    return client


def subscribe_for_input(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"input received: {msg.payload.decode()}")
        output = process_sales_man(msg.payload.decode())
        out_bound_client_instance = connect_outbound_mqtt()
        publish(out_bound_client_instance, settings.MQTT_RESULT_TOPIC, output, retain=True)

    client.subscribe(settings.MQTT_REQUEST_TOPIC)
    client.on_message = on_message


def publish(client, topic, msg, retain=False):
    result = client.publish(topic, qos=1, retain=retain, payload=msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def subscribe(client, topic):
    def on_message(client, userdata, msg):
        print(msg.payload.decode())
    client.subscribe(topic)
    client.on_message = on_message
    print("subscribing...")
    try:
        while True:
            client.loop(1000)
    except:
        client.disconnect()
        print("exited")


def run_bounds():
    in_bound_client_instance = connect_inbound_mqtt()
    subscribe_for_input(in_bound_client_instance)
    print("running...")
    try:
        while True:
            in_bound_client_instance.loop(1000)
    except:
        in_bound_client_instance.disconnect()
        print("exited")
