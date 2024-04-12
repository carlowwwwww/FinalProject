import json
from paho.mqtt import client as mqtt_client
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt
import time

broker = 'localhost'
port = 1883
topic = "humidity"

dataStorage = []
plt.figure(figsize=(8, 4.5))
plt.title('Real-time Humidity Sensor Data')


def on_message(client, userdata, msg):
    global dataStorage
    try:
        data = json.loads(msg.payload.decode())
    except:
        # Handles missing data
        values = [d['value'] for d in dataStorage[-5:]]
        data = {"id": 000,
                "device_name": f"Sensor_UNKNOWN",
                "timestamp": time.asctime(),
                "value": sum(values) / len(values)}

        print(f"appended {data['value']}")
    dataStorage.append(data)
    dataStorage = dataStorage[-150:]


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client("Subscriber")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    return client


def updatePlot(frame):
    plt.clf()  # Clear previous plot
    plt.title('Real-time Humidity Sensor Data')
    plt.ylabel('Humidity (%)')
    if dataStorage:  # Check if there's data in dataStorage
        values = [data['value'] for data in dataStorage[-100:]]
        plt.plot(movingAverage(values, 3))
        plt.xlabel(f'Latest Humidity: {round(values[-1], 2)}%')
        plt.xlim(0, len(values))
        plt.ylim((min(values) - 10, max(values) + 10))


# Added to make the data look smoother
def movingAverage(data, smoothing):
    smoothedData = []
    for i in range(len(data) - smoothing + 1):
        window = data[i:i + smoothing]
        smoothedData.append(sum(window) / smoothing)
    return smoothedData


def run():
    client = connect_mqtt()
    client.connect(broker, port)
    client.subscribe(topic)
    client.loop_start()
    ani = FuncAnimation(plt.gcf(), updatePlot, interval=1000, cache_frame_data=False)
    plt.show()


if __name__ == '__main__':
    run()
