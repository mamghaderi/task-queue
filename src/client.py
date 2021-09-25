import settings
import mqtt_backend
cl1 = mqtt_backend.connect_inbound_mqtt()
mqtt_backend.publish(cl1, settings.MQTT_REQUEST_TOPIC, '[[1,4], [3,9], [23,45], [5,18]]')
cl2 = mqtt_backend.connect_outbound_mqtt()
mqtt_backend.subscribe(cl2, settings.MQTT_RESULT_TOPIC)
