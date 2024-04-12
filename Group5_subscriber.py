import json
from paho.mqtt import client as mqtt_client
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt
import time

broker = 'localhost'
port = 1883
topic_base = "humidity/#"

dataStorage = {}

plt.figure(figsize=(10, 6))
plt.title('Real-time Humidity Sensor Data Across Locations')


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        location = data['location']
        if location not in dataStorage:
            dataStorage[location] = []
        dataStorage[location].append(data)
        dataStorage[location] = dataStorage[location][-150:]
    except Exception as e:
        print(f"Error processing message: {e}")


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(topic_base)
        else:
            print(f"Failed to connect, return code {rc}\n")

    client = mqtt_client.Client("Subscriber")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    return client


def updatePlot(frame):
    plt.clf()
    plt.title('Real-time Humidity Sensor Data Across Locations')
    plt.ylabel('Humidity (%)')
    has_data = False
    for location, records in dataStorage.items():
        if records:
            values = [record['value'] for record in records]
            plt.plot(movingAverage(values, 3), label=f'{location}')
            has_data = True
    plt.xlabel('Time')
    if has_data:
        plt.legend(loc='upper left')
    plt.ylim(30, 90)


def movingAverage(data, smoothing):
    smoothedData = []
    for i in range(len(data) - smoothing + 1):
        window = data[i:i + smoothing]
        smoothedData.append(sum(window) / smoothing)
    return smoothedData


def run():
    client = connect_mqtt()
    client.loop_start()
    ani = FuncAnimation(plt.gcf(), updatePlot, interval=1000, cache_frame_data=False)
    plt.show()


if __name__ == '__main__':
    run()
