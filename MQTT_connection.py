from umqtt.simple import MQTTClient
import time
import machine
mqtt_server = 'broker.hivemq.com'
client_id = 'pi4'
topic_pub = b'LabHardware'
topic_msg = b'Toggle Led'

def init_connection():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client
