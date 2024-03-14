import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

def init_connection(ssid: str, key: str):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, key)
    time.sleep(5)
    print(wlan.isconnected())