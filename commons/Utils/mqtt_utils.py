# encoding=utf8

import hashlib
import paho.mqtt.client as mqtt

# from commons.Utils.log_utils import getLogger
# log = getLogger('mqtt_utils')

# MQTT_HOST = '115.28.110.241'
MQTT_HOST = '120.55.95.153'
MQTT_PORT = 1883
SECRET_KEY = '3444462b-0f6f-4523-b382-92a1288345ef'

MQTT_CLIENT = None


def get_mqtt_client():
    global MQTT_CLIENT
    MQTT_CLIENT = None
    if not MQTT_CLIENT:
        MQTT_CLIENT = mqtt.Client()
        MQTT_CLIENT.reinitialise()
        MQTT_CLIENT.connect(MQTT_HOST, MQTT_PORT)
    return MQTT_CLIENT


def send_msg(topic, msg):
    client = get_mqtt_client()
    topic1 = topic_encode(topic)
    client.publish(topic1, msg)


def watch_msg(topic, handler):
    def on_connect(client, userdata, flags, rc):
        # log.debug("Start watching topic {0} ...".format(topic))
        topic1 = topic_encode(topic)
        client.subscribe(topic1)

    def on_message(client, userdata, msg):
        handler(str(msg.payload).decode('utf8'))

    client = get_mqtt_client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()


def topic_encode(topic):
    return hashlib.md5(topic + SECRET_KEY).hexdigest()
