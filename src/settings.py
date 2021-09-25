import random


MQTT_BROKER = 'broker.emqx.io'
MQTT_PORT = 1883
MQTT_REQUEST_TOPIC = "serveh/test/request"
MQTT_RESULT_TOPIC = "serveh/test/result"
INBOUND_CLIENT_ID = f'inbound-{random.randint(0, 1000)}'
OUTBOUND_CLIENT_ID = f'outbound-{random.randint(0, 1000)}'
