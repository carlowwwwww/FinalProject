# import random
# import time
#
# start_id = 111
#
#
# def create_data(device_id):
#     return {
#         'id': device_id,
#         'device_name': f"Sensor_{device_id}",
#         'timestamp': time.asctime(),
#         'temperature': round(random.uniform(20, 30), 2),
#         'humidity': round(random.uniform(40, 60), 2),
#         'air_quality': {
#             'pm2_5': round(random.uniform(10, 50), 2),
#             'pm10': round(random.uniform(20, 100), 2)
#         },
#         'battery_level': random.randint(10, 100),
#         'status': 'Active' if random.random() > 0.1 else 'Inactive'
#     }
#
#
# def print_data(data):
#     print("ID:", data['id'])
#     print("Device Name:", data['device_name'])
#     print("Timestamp:", data['timestamp'])
#     print("Temperature:", data['temperature'], "°C")
#     print("Humidity:", data['humidity'], "%")
#     print("Air Quality:")
#     print("  PM2.5:", data['air_quality']['pm2_5'], "µg/m³")
#     print("  PM10:", data['air_quality']['pm10'], "µg/m³")
#     print("Battery Level:", data['battery_level'], "%")
#     print("Status:", data['status'])
#     print()
