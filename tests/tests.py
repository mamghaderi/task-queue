import unittest
import time
from paho.mqtt import client as mqtt_client
from src import settings


class TestBrokerConnection(unittest.TestCase):
    def setUp(self):
        self.client = mqtt_client.Client("Test Client")
        self.client.on_connect = self.on_connect
        self.broker = settings.MQTT_BROKER
        self.port = settings.MQTT_PORT
        self.has_connected = False

    def on_connect(self, client, userdata, flags, rc):  # connect function
        if rc == 0:
            self.has_connected = True

    def test_connection(self):  # test to check connection to broker
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        time.sleep(2)
        self.client.loop_stop()
        self.assertTrue(self.has_connected)


if __name__ == '__main__':
    unittest.main()
