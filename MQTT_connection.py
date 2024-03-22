from umqtt.simple import MQTTClient
import time
import machine
#mqtt_server = 'broker.hivemq.com'
mqtt_broker = '192.168.100.152'
#mqtt_user = 'raspberry_pi_pico_w'

def init_connection():
    client = MQTTClient("raspberry_pi_pico_w", mqtt_broker, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker')
    return client
