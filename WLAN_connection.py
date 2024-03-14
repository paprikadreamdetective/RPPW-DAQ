import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

def init_connection(ssid: str, key: str) -> network:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, key)
    return wlan
    #print(wlan.isconnected())
    #time.sleep(5)