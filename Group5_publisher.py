import json
import random
import time
import threading
from paho.mqtt import client as mqtt_client
from Group5_data_generator import Sensor


class Publisher:
    def __init__(self, broker, port, client_id, location, topic_base="humidity"):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.location = location
        self.topic = f"{topic_base}/{location}"
        self.sensor = Sensor()
        self.client = self.connect_mqtt()

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"Connected to MQTT Broker as {self.client_id}!")
            else:
                print(f"Failed to connect, return code {rc}\n")

        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self):
        while True:
            data = {
                "id": self.client_id,
                "location": self.location,
                "timestamp": time.asctime(),
                "value": self.sensor.normalizeValue
            }

            msg = json.dumps(data)
            self.client.publish(self.topic, msg)
            time.sleep(0.5)


def run():
    locations = ['Toronto', 'Vancouver', 'Montreal', 'Calgary']
    client_ids = ['Publisher1', 'Publisher2', 'Publisher3', 'Publisher4']
    threads = []

    for location, client_id in zip(locations, client_ids):
        publisher = Publisher('localhost', 1883, client_id, location)
        thread = threading.Thread(target=publisher.publish)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    run()
