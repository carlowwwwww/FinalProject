import json
import random
import time
from paho.mqtt import client as mqtt_client
from Group5_data_generator import Sensor


class Publisher:
    def __init__(self, broker, port, start_id, topic):
        self.broker = broker
        self.port = port
        self.start_id = start_id
        self.client = self.connect_mqtt()
        self.topic = topic
        self.sensor = Sensor(delta=0.07)

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client("Publisher")
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self):
        while True:
            # self.start_id += 1
            # data = util.create_data(self.start_id)
            data = {"id": self.start_id,
                    "device_name": f"Sensor_{self.start_id}",
                    "timestamp": time.asctime(),
                    "value": self.sensor.normalizeValue}

            msg = json.dumps(data)

            # Simulate missing data 1/100 times
            isMissing = random.randint(1, 100) == 1
            if isMissing:
                self.client.publish(self.topic, None)
            else:
                self.client.publish(self.topic, msg)

            time.sleep(0.5)


def run():
    publisher = Publisher('localhost', 1883, 100, "humidity")
    publisher.publish()


if __name__ == '__main__':
    run()
