import logging
import threading
import json
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage

from variables import variables
from handlers.factory import factory

# Callback when the client connects to the broker
# pylint: disable-next=unused-argument
def on_connect(client : mqtt.Client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT broker")

        # Subscribe to the desired topic
        for entry in factory.handlers.items():
            handler = entry[1]
            result = client.subscribe(handler.handler_code(), 1)
            logging.info("Subscribe to topic: %s with results: %s", handler.handler_code(), result)
    else:
        logging.error("Connection failed with code: %s", rc)

# pylint: disable-next=unused-argument
def on_message(client, userdata, message: MQTTMessage):
    payloadJson = json.loads(message.payload.decode("utf-8"))
    logging.info("Received message: %s from topic: %s", payloadJson, message.topic)
    factory.resolve_handler(message.topic).handle(payloadJson)

# pylint: disable-next=unused-argument
def on_publish(client, userdata, mid):
    logging.info("Publish: %s", mid)

# pylint: disable-next=unused-argument
def on_disconnect(client, userdata, rc):
    logging.info("Disconnected from MQTT broker")

mqtt_client = mqtt.Client()

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_publish = on_publish

class MessageListener:
    def __init__(self) -> None:
        self._task = threading.Thread(target=self._run_task)
        self.stopping = threading.Event()

    def start(self):
        try:
            self._task.start()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        logging.info("Closing connection")
        self.stopping.set()
        mqtt_client.disconnect()

    def _run_task(self):
        logging.info("Starting connection to the: %s", variables.mq_host())
        status = mqtt_client.connect(variables.mq_host())
        logging.info("connection statis is: %s", status)
        mqtt_client.loop_forever()